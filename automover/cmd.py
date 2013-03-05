import os
import argparse
import logging
import subprocess
import ConfigParser

from automover.sections import SECTIONS
from automover.clients import CLIENTS
from automover.remover import handle_remove

logger = logging.getLogger(__name__)

def commandline_handler():
    parser = argparse.ArgumentParser(description='Check for stuff to automove.')
    parser.add_argument("config", help="Path to config file", type=str)

    args = parser.parse_args()
    if not os.path.isfile(args.config):
        print 'File not found: %s' % args.config
        quit()

    config = ConfigParser.RawConfigParser()
    config.read(args.config)

    moved_something = False
    
    all_destination_paths = []
    section_types = dict((k.name, k) for k in SECTIONS)
    client_types = dict((k.name, k) for k in CLIENTS)
    
    sections = []
    clients = {}
    
    for section in config.sections():
        if section == 'general':
            execute_on_moved = config.has_option('general', 'execute_on_moved') and config.get('general', 'execute_on_moved') or None
        elif section == 'remover':
            remover_sites = {}
        
            for site in [x for x in config.options(section) if not x.endswith('_ratio') and not x.endswith('_time')]:
                if config.has_option(section, '%s_ratio' % site):
                    t = 'ratio'
                    remover_sites[site] = ('ratio', config.get(section, site).lower(), config.getfloat(section, '%s_ratio' % site))
                elif config.has_option(section, '%s_time' % site):
                    t = 'time'
                else:
                    logger.warn('Missing a ratio or time for site %s', site)
                    continue
                
                remover_sites[site] = (t, config.get(section, site).lower(), config.getfloat(section, '%s_%s' % (site, t)))
                
        elif section.startswith('client_'):
            t = config.get(section, 'type')
            klass = client_types.get(t, None)
            if not klass:
                logger.error('Unknown type for client: %s', t)
                continue
            
            config.remove_option(section, 'type')
            clients[name] = klass(**dict(config.items(section)))
            
        elif section.startswith('section_'):
            t = config.get(section, 'type')
            klass = section_types.get(t, None)
            if not klass:
                logger.error('Unknown type for section: %s', t)
                continue
            
            sec = {
                'name': '_'.join(section.split('_')[1:]),
                'klass': klass,
                'target_paths': filter(lambda x:x, config.get(section, 'target_paths').split(',')),
                'source_paths': filter(lambda x:x, config.get(section, 'source_paths').split(',')),
                'automove_syntax': config.has_option(section, 'automove_syntax') and config.get(section, 'automove_syntax') or None,
            }
            
            sections.append(sec)
            all_destination_paths.extend(sec['target_paths'])
        else:
            logger.error('Unknown file section: %s', section)
        
    moved_something = False
    for client_name, client in clients.items():
        for section in sections:
            logger.info('Looking for something to do with client %s in section %s', client_name, section['name'])
            klass = section['klass']    
            sec = klass(
                section['source_paths'],
                section['destination_paths'],
                section['automove_syntax']
            )
            sec.scan(client)
        
    if remover_sites:
        logger.debug('Looking for torrents to remove')
        handle_remove(client, remover_sites, all_destination_paths)

if __name__ == '__main__':
    commandline_handler()