import os
import logging

from automover.utils import get_free_space


class Automover(object):
    def __init__(self, source_paths, destination_paths, automove_syntax, test_mode=False):
        self.source_paths = source_paths
        self.destination_paths = destination_paths
        self.automove_syntax = automove_syntax
        self.test_mode = test_mode
        
        self.logger = logging.getLogger(__name__)
    
    def get_free_space(self, p):
        return get_free_space(p)
    
    def scan(self, client):
        moved_anything = False
        
        self.logger.debug('Scanning section %s with client %s' % (self.name, client.name))
        for torrent in client.list():
            for source_path in self.source_paths:
                if torrent.path.startswith(source_path):
                    self.logger.debug('%s matches %s' % (torrent.path, source_path))
                    break
            else:
                continue

            if not torrent.is_complete:
                self.logger.debug('%s is not complete' % torrent)
                continue

            name = torrent.name
            size = torrent.get_size()

            destination_paths = [p for p in self.destination_paths if self.get_free_space(p) - 10*1024*1024 > size]
            if not destination_paths:
                self.logger.debug('No free space for %s (need %s)' % (torrent, size))
                continue

            if self.automove_syntax:
                check_dirs = destination_paths # find best path in these
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
                
                destination = os.path.join(sorted(check_dirs, key=check_part_count, reverse=True)[0], target)
            else:
                destination = destination_paths[0]
            
            if not os.path.isdir(destination):
                os.makedirs(destination)

            self.logger.debug('Moving %s to %s' % (name, destination))
            if not self.test_mode:
                torrent.move(destination)
            moved_anything = True
        
        return moved_anything

    def cleanup_part(self, part):
        return part.replace('_', '').replace('.', '').replace(' ', '').lower()

    def get_interpolation_variables(self, name):
        raise NotImplementedError('Method must be implemented to move files')
