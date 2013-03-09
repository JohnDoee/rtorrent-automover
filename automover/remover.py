import logging
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)

def handle_remove(client, remover_sites, target_paths, test_mode=False):
    for torrent in client.list():
        if not torrent.is_complete:
            logging.debug('%s is not complete, skipping' % torrent)
            continue
        
        for target_path in target_paths:
            if torrent.path.startswith(target_path):
                break
        else:
            logger.debug('%s is not in any known path, skipping' % torrent)
            continue
        
        deleted = False
        for tracker in torrent.trackers():
            for site, (t, url, limit) in remover_sites.items():
                if url in tracker.lower():
                    if t == 'ratio':
                        if limit <= torrent.ratio:
                            logging.debug('Torrent %s was seeded %s and only %s is required, removing' % (torrent, torrent.ratio, limit))
                            if not test_mode:
                                torrent.delete()
                            deleted = True
                            break
                    elif t == 'time':
                        if datetime.now()-timedelta(hours=int(limit)) > torrent.finish_time:
                            logging.debug('Torrent %s was finished at %s' % (torrent, torrent.finish_time))
                            if not test_mode:
                                torrent.delete()
                            deleted = True
                            break
            if deleted:
                break