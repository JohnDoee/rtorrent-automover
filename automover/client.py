import os
import shutil
import logging

from automover.utils import get_size

class Torrent(object):
    """A torrent file as returned by client"""
    
    def __init__(self, client, torrent_id, finish_time, ratio, path, is_complete):
        """A torrent file.
        
        :param client: Torrent client to interact with.
        :type client: Client.
        :param torrent_id: The ID to identify the torrent by.
        :type torrent_id: str.
        :param finish_time: Time the torrent was finished.
        :type finish_time: datetime.datetime.
        :param ratio: Upload/Download ratio.
        :type ratio: float.
        :param path: Path to the torrent file.
        :type path: str.
        :param is_complete: Torrent is complete.
        :type is_complete: bool.
        """
        self.client = client
        self.torrent_id = torrent_id
        self.finish_time = finish_time
        self.ratio = ratio
        self.path = path
        self.is_complete = is_complete
        self.logger = logging.getLogger(__name__)
        
        self.name = os.path.split(path)[1]
    
    def _move(self, path, destination_path):
        shutil.move(self.path, destination_path)
    
    def move(self, destination):
        destination_path = os.path.join(destination, self.name)
        if os.path.isfile(destination_path) or os.path.isdir(destination_path):
            self.logger.error('Unable to move %s because %s already exists', self.name, destination_path)
            return False
        
        self.client.stop(self)
        
        self.client.set_path(self, destination)
        self._move(self.path, destination_path)
        self.path = destination
        self.client.start(self)
        
        self.logger.info('Moved %s to %s', self.name, destination)
    
    def delete(self):
        return self.client.delete(self)
    
    def trackers(self):
        return self.client.trackers(self)
    
    def get_size(self):
        return get_size(self.path)
    
    def __repr__(self):
        return 'Torrent("%s", "%s")' % (self.torrent_id, self.path)
    
    

class Client(object):
    """
    Generic torrent client with all the needed bells and whistles not implemented.
    """
    
    def list(self):
        """Returns list of all torrents in client with information.
        
        :returns: list of Torrent.
        """
        raise NotImplemented()
    
    def delete(self, torrent):
        """Deletes a torrent
        
        :param torrent: A torrent file object.
        :type torrent: Torrent.
        :returns: bool -- Delete was successful.
        """
        raise NotImplemented()
    
    def stop(self, torrent):
        """Stops a torrent
        
        :param torrent: A torrent file object.
        :type torrent: Torrent.
        :returns: bool -- Stop was successful.
        """
        raise NotImplemented()
    
    def start(self, torrent):
        """Starts a torrent
        
        :param torrent: A torrent file object.
        :type torrent: Torrent.
        :returns: bool -- Start was successful.
        """
        raise NotImplemented()
    
    def set_path(self, torrent, path):
        """Sets a part for a torrent
        
        :param torrent: A torrent file object.
        :type torrent: Torrent.
        :param path: Path to file location.
        :type path: str.
        :returns: bool -- Change path was successful.
        """
        raise NotImplemented()
    
    def trackers(self, torrent):
        """Sets a part for a torrent
        
        :param torrent: A torrent file object.
        :type torrent: Torrent.
        :returns: list of strs -- List of torrent trackers.
        """
        raise NotImplemented()
