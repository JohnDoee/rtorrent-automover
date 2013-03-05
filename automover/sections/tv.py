import re

from automover.section import Automover

class TVAutomover(Automover):
    """
    Moves TV to correct subfolders
    """
    name = 'tv'

    def get_interpolation_variables(self, name):
        matchers = [
            r'(?i)(?P<show>.+?)[_.-]S(?P<season>\d+)[_.-]?E(?P<episode>\d+)[E_.-]',
            r'(?i)(?P<show>.+?)[_.-](?P<season>\d+)x(?P<episode>\d+)[E_.-]',
            r'(?i)(?P<show>.+?)[_.-](?P<season>20[01][0-9])[_.-](?P<episode>[01]?[0-9][_.-][0-3]?[0-9])[_.-]',
            r'(?i)(?P<show>.+?)[_.-]?E(?P<episode>\d+)[E_.-]'
        ]

        for m in matchers:
            result = re.match(m, name)
            if result:
                if 'season' in result.groupdict():
                    season = int(result.group('season'))
                else:
                    season = 1
                break
        else:
            return {}

        return {'show': result.group('show'), 'season': season, 'episode': int(result.group('episode').replace('_', '').replace('.', '').replace('-', ''))}