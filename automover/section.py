#!/usr/bin/env python

import argparse
import os
import ConfigParser
import logging
import re
import time
import subprocess
import shutil


class Automover(object):
    def __init__(self, source_paths, destination_paths, automove_syntax):
        self.source_paths = source_paths
        self.destination_paths = destination_paths
        self.automove_syntax = automove_syntax
        
        self.logger = logging.getLogger(__name__)

    def scan(self, client):
        moved_anything = False
        
        self.logger.debug('Scanning section: %s' % self.name)
        for torrent in client.list():
            for source_path in self.source_paths:
                if torrent.path.startswith(source_path):
                    self.logger.debug('%s matches %s' % (torrent.path, source_path))
                    break
            else:
                continue

            if not torrent.is_complete(f):
                self.logger.debug('%s is not complete' % f)
                continue

            name = torrent.name
            size = torrent.get_size()

            destination_paths = [p for p in self.destination_paths if get_free_space(p) + 10*1024*1024 > size]

            check_dirs = destination_paths # find best path in these
            if self.automove_syntax:
                target = self.automove_syntax % self.get_interpolation_variables(name)
                target_split = target.strip(os.sep).split(os.sep)
                
                def check_part_count(f):
                    i = 0
                    for t in target_split:
                        useful_paths = [x for x in os.listdir(f) if self.cleanup_part(x) == self.cleanup_part(t)]
                        
                        if not useful_paths:
                            break
                        
                        f = os.path.join(f, useful_paths[0])
                        i += 1
                    return i
                
                check_dirs = sorted(check_dirs, key=check_part_count, reverse=True)
            destination = check_dirs[0]
            
            if not os.path.isdir(destination):
                os.makedirs(destination)

            self.logger.debug('Moving %s to %s' % (name, destination))
            torrent.move(destination)
            moved_anything = True
        
        return moved_anything

    def cleanup_part(self, part):
        return part.replace('_', '').replace('.', '').replace(' ', '').lower()

    def get_interpolation_variables(self, name):
        raise NotImplementedError('Method must be implemented to move files')