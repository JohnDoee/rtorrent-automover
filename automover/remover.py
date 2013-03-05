import logging
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)

def handle_remove(client, remover_sites, target_paths):
    for torrent in client.list():
        if not torrent.is_complete:
            logging.debug('%s is not complete' % torrent)
            continue
        
        for target_path in target_paths:
            if torrent.path.startswith(target_path):
                break
        else:
            logger.debug('%s is not moved yet' % f)
            continue
        
        #trackers = [proxy.t.get_url('%s:t%s' % (f, i)) for i in range(proxy.d.get_tracker_size(f))]
        #
        checked = False
        for tracker in torrent.trackers():
            for site, (t, url, limit) in remover_sites.items():
                if url in tracker.lower():
                    if t == 'ratio':
                        if limit <= torrent.ratio:
                            logging.debug('Torrent %s was seeded %s and only %s is required, removing' % (f, torrent.ratio, limit))
                            torrent.delete()
                        break
                        checked = True
                    elif t == 'time':
                        if datetime.now()-timedelta(hours=int(limit)) > torrent.finish_time:
                            logging.debug('Torrent %s was finished at %s' % (f, torrent.finish_time))
                            torrent.delete()
                        break
                        checked = True
            if checked:
                break
        
        if not checked:
            logging.debug('%s is not on any known tracker' % f)