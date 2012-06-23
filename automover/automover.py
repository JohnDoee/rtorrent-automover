#!/usr/bin/env python

import argparse
import os
import ConfigParser
import logging
import sys
import re
import time
import subprocess

from xmlrpclib import ServerProxy
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class Automover(object):
    def __init__(self, xmlrpc_url, source_paths, destination_paths, automove_syntax):
        self.source_paths = source_paths
        self.destination_paths = destination_paths
        self.proxy = ServerProxy(xmlrpc_url)
        self.automove_syntax = automove_syntax

    def scan(self):
        moved_anything = False
        
        logging.debug('Scanning section: %s' % self.name)
        for f in self.proxy.download_list():
            directory = self.proxy.d.directory(f)
            for source_path in self.source_paths:
                if directory.startswith(source_path):
                    logging.debug('%s matches %s' % (directory, source_path))
                    break
            else:
                continue

            if not self.proxy.d.get_complete(f):
                logging.debug('%s is not complete' % f)
                continue

            name = self.proxy.d.name(f)

            if self.automove_syntax:
                target = self.automove_syntax % self.get_interpolation_variables(name)
                check_dirs = self.destination_paths
                for part in target.strip(os.sep).split(os.sep):
                    check_part = self.cleanup_part(part)
                    result_dirs = []
                    for check_dir in check_dirs:
                        result_dirs += map(lambda x:os.path.join(check_dir, x[1]), filter(lambda x:x[0] == check_part, map(lambda x:(self.cleanup_part(x), x), os.listdir(check_dir))))
                    check_dirs = result_dirs

                if check_dirs:
                    destination = check_dirs[0]
                    logging.debug('Using already existing %s' % destination)
                else:
                    destination = os.path.join(self.destination_paths[0], target)
                    os.makedirs(destination)
                    logging.debug('Creating directory %s' % destination)

            else:
                destination = self.destination_paths[0]

            if not os.path.isdir(destination):
                logging.warning('Not moving %s because %s does not exist' % (name, destination))

            logging.debug('Moving %s to %s' % (name, destination))
            self.move_hash(f, destination)
            moved_anything = True
        
        return moved_anything

    def cleanup_part(self, part):
        return part.replace('_', '').replace('.', '').replace(' ', '').lower()

    def get_interpolation_variables(self, name):
        raise NotImplementedError('Method must be implemented to move files')

    def get_state(self, hash):
        return self.proxy.d.state(hash)

    def stop_torrent(self, hash):
        logging.debug('Stopping torrent')
        self.proxy.d.stop(hash)

        while self.get_state(hash) != 0:
            time.sleep(0.5)

        logging.debug('Torrent stopped')

    def start_torrent(self, hash):
        logging.debug('Starting torrent')
        self.proxy.d.start(hash)

        while self.get_state(hash) != 1:
            time.sleep(0.5)

        logging.debug('Torrent started')


    def move_hash(self, hash, destination):
        is_started = self.proxy.d.state(hash)
        source = self.proxy.d.directory(hash)
        destination_name = os.path.join(destination, self.proxy.d.name(hash))
        if os.path.isdir(destination_name):
            logging.error('Target folder %s already exist' % destination_name)
            return

        if is_started:
            self.stop_torrent(hash)
        self.proxy.d.set_directory(hash, destination)
        os.rename(source, destination_name)

        if is_started:
            self.start_torrent(hash)
        logging.debug('Moved torrent %s' % self.proxy.d.name(hash))


class TVAutomover(Automover):
    name = 'tv'

    def get_interpolation_variables(self, name):
        result = re.match(r'(?i)(?P<show>.+?)(?:\.|_?:)S0*(?P<season>\d+)E0*(?P<episode>\d+)(?:\.|_?:)', name)

        if not result:
            return None

        return {'show': result.group('show'), 'season': int(result.group('season')), 'episode': int(result.group('episode'))}


class MoviesAutomover(Automover):
    name = 'movies'


def commandline_handler():
    parser = argparse.ArgumentParser(description='Check for stuff to automove.')
    parser.add_argument("config", help="Path to config file", type=str)

    args = parser.parse_args()
    if not os.path.isfile(args.config):
        print 'File not found: %s' % args.config
        quit()

    config = ConfigParser.RawConfigParser()
    config.read(args.config)

    xmlrpc_url = config.get('general', 'xmlrpc_url')

    moved_something = False
    
    for klass in [TVAutomover, MoviesAutomover]:
        section = klass.name
        if not config.has_section(section):
            continue

        automove_syntax = config.has_option(section, 'automove_syntax') and config.get(section, 'automove_syntax') or None
        automover = klass(xmlrpc_url,
                            config.get(section, 'source_paths').split(','),
                            config.get(section, 'target_paths').split(','),
                            automove_syntax)
        result = automover.scan()
        if not moved_something:
            moved_something = result
    
    if moved_something and config.has_option('general', 'execute_on_moved'):
        subprocess.call(config.get('general', 'execute_on_moved'), shell=True)

if __name__ == '__main__':
    commandline_handler()
