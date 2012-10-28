from urllib.request import urlopen
from bs4 import BeautifulSoup, UnicodeDammit
import re
from ModuleBase import *


class Air(object):
    ''' module for checking air time of anime '''

    url = 'http://www.mahou.org/Showtime'
    user_db = 'anime_aliases.json'

    def alias_anime(self, anime, alias):
        animalias = register_name_(anime, alias, self.user_db)
        return animalias

    def lookup_show(self, show):
        query = ' '.join(show)
        anime = check_alias(query, self.user_db)
        lookup_re = re.compile('^' + re.escape(anime), re.I)
        eta_re = re.compile('^[0-9]{1,2}[wdhm]\s')
        data = urlopen(self.url)
        soup = BeautifulSoup(data.read())

        try:
            shows = soup.find('table', attrs={'summary' : 'Currently Airing'}) #.find_next('table', {'summary': ''}).next_element
            show_name = shows.find_next(text=lookup_re) #Nisemonogatari
            eta = show_name.parent.find_next(text=eta_re)
            #eta = show_name.parent.find_next_siblings('td')[4]
        except AttributeError as e:
            return 'No show by that name was found. Try http://www.mahou.org/Showtime/ for a list of shows.'

        if eta != None:
            return '{0} will air in {1}'.format(anime, eta)
        else:
            return 'No eta found for {}'.format(anime)