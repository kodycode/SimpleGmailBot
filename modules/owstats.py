from bs4 import BeautifulSoup
import urllib.request

class OWStats:

    def __init__(self, battle_tag):
        self.battle_tag = battle_tag.replace('-','#')
        self.skill_rating = 0
        self.level = 0
        self.wins = 0
        self.ranked_wins = 0
        self.losses = 0
        self.ranked_losses = 0
        self.win_percentage = 0
        self.ranked_win_percentage = 0
        self.time_played = 0
        self.ranked_time_played = 0
        self.top_heroes = []
        self.ranked_top_heroes = []
        self.top_hours = []
        self.ranked_top_hours = []
        self.URL = 'https://playoverwatch.com/en-us/career/pc/us/' + battle_tag
        self.html_source = urllib.request.urlopen(self.URL)
        self.soup = BeautifulSoup(self.html_source, 'html.parser')

    def get_skill_rating(self):
        try:
            rank = self.soup.find('div', {'class': 'competitive-rank'})
            rating = rank.find('div', {'class': 'u-align-center h6'})
            self.skill_rating = str(rating.text)

        except AttributeError as e:
            self.skill_rating = 'Skill Rating not found'

    def get_wins(self):
        table = self.soup.find_all('table', {'class': 'data-table'})
        td = table[6].find_all('td')

        self.wins = td[1].text.replace(',','')

    def get_ranked_wins(self):
        for competitive in self.soup.find('div', {'id': 'competitive-play'}):
            table = competitive.find_all('table', {'class': 'data-table'})

        td = table[6].find_all('td')

        self.ranked_wins = td[1].text.replace(',','')

    def get_losses(self):
        table = self.soup.find_all('table', {'class': 'data-table'})
        td = table[6].find_all('td')

        self.losses = int(td[3].text.replace(',','')) - int(td[1].text.replace(',',''))
        self.losses = str(self.losses)

    def get_ranked_losses(self):
        for competitive in self.soup.find('div', {'id': 'competitive-play'}):
            table = competitive.find_all('table', {'class': 'data-table'})

        td = table[6].find_all('td')

        self.ranked_losses = int(td[3].text.replace(',','')) - int(td[1].text.replace(',',''))
        self.ranked_losses = str(self.ranked_losses)

    def get_win_percentage(self):
        table = self.soup.find_all('table', {'class': 'data-table'})
        td = table[6].find_all('td')

        wins = int(td[1].text.replace(',',''))
        total_games = int(td[3].text.replace(',',''))

        self.win_percentage = (wins/total_games) * 100

    def get_ranked_win_percentage(self):
        for competitive in self.soup.find('div', {'id': 'competitive-play'}):
            table = competitive.find_all('table', {'class': 'data-table'})

        td = table[6].find_all('td')

        wins = int(td[1].text.replace(',',''))
        total_games = int(td[3].text.replace(',',''))

        self.ranked_win_percentage = (wins/total_games) * 100

    def get_time_played(self):
        table = self.soup.find_all('table', {'class': 'data-table'})
        td = table[6].find_all('td')

        #Checks if profile is still using score metrics
        if (len(td) == 12):
            self.time_played = td[11].text
        else:
            self.time_played = td[9].text

    def get_ranked_time_played(self):
        for competitive in self.soup.find('div', {'id': 'competitive-play'}):
            table = competitive.find_all('table', {'class': 'data-table'})

        td = table[6].find_all('td')

        #Checks if profile is still using score metrics
        if (len(td) == 12):
            self.ranked_time_played = td[11].text
        else:
            self.ranked_time_played = td[9].text

    def get_total_time_played(self):
        ### Quick Play Time
        table = self.soup.find_all('table', {'class': 'data-table'})
        td = table[6].find_all('td')

        #Checks if profile is still using score metrics
        if (len(td) == 12):
            time_played1 = td[11].text.replace(' hours', '')
        else:
            time_played1 = td[9].text.replace(' hours', '')

        ### Competitive Play Time
        for competitive in self.soup.find('div', {'id': 'competitive-play'}):
            table = competitive.find_all('table', {'class': 'data-table'})

        td = table[6].find_all('td')

        #Checks if profile is still using score metrics
        if (len(td) == 12):
            time_played2 = td[11].text.replace(' hours', '')
        else:
            time_played2 = td[9].text.replace(' hours', '')

        self.total_time_played = str(int(time_played1) + int(time_played2))

    def get_level(self):
        level = self.soup.find('div', {'class': 'u-vertical-center'})

        prestige1 = self.soup.find('div', {'style': 'background-image:url(https://' +
                                     'blzgdapipro-a.akamaihd.net/game/playerlevelrewards/0x025000000000092B_Rank.png)'})
        prestige2 = self.soup.find('div', {'style': 'background-image:url(https://' +
                                      'blzgdapipro-a.akamaihd.net/game/playerlevelrewards/0x0250000000000951_Rank.png)'})
        prestige3 = self.soup.find('div', {'style': 'background-image:url(https://' +
                                      'blzgdapipro-a.akamaihd.net/game/playerlevelrewards/0x0250000000000952_Rank.png)'})
        prestige4 = self.soup.find('div', {'style': 'background-image:url(https://' +
                                      'blzgdapipro-a.akamaihd.net/game/playerlevelrewards/0x0250000000000953_Rank.png)'})
        prestige5 = self.soup.find('div', {'style': 'background-image:url(https://' +
                                      'blzgdapipro-a.akamaihd.net/game/playerlevelrewards/0x0250000000000954_Rank.png)'})

        if (prestige1):
            self.level = str(int(level.text) + int(100))
        elif (prestige2):
            self.level = str(int(level.text) + int(200))
        elif (prestige3):
            self.level = str(int(level.text) + int(300))
        elif (prestige4):
            self.level = str(int(level.text) + int(400))
        elif (prestige5):
            self.level = str(int(level.text) + int(500))
        else:
            self.level = str(level.text)

    def get_top_five_heroes(self):
        count = 0
        for competitive in self.soup.find_all('div', {'id': 'quick-play'}):
            for bar in self.soup.find_all('div', {'class': 'bar-text'}):
                if (count == 5):
                    break

                for hero in bar.find_all('div', {'class': 'title'}):
                    self.top_heroes.append(str(hero.text))

                count = count+1

    def get_ranked_top_five_heroes(self):
        count = 0

        for competitive in self.soup.find_all('div', {'id': 'competitive-play'}):
            for bar in competitive.find_all('div', {'class': 'bar-text'}):
                if (count == 5):
                    break

                for hero in bar.find_all('div', {'class': 'title'}):
                    self.ranked_top_heroes.append(str(hero.text))

                count = count + 1

    def get_top_five_heroes_hours(self):
        count = 0

        for bar in self.soup.find_all('div', {'class': 'bar-text'}):
            if (count == 5):
                break

            for hours in bar.find_all('div', {'class': 'description'}):
                self.top_hours.append(str(hours.text))

            count = count+1

    def get_ranked_top_five_heroes_hours(self):
        count = 0

        for competitive in self.soup.find_all('div', {'id': 'competitive-play'}):
            for bar in competitive.find_all('div', {'class': 'bar-text'}):
                if (count == 5):
                    break

                for hours in bar.find_all('div', {'class': 'description'}):
                    self.ranked_top_hours.append(str(hours.text))

                count = count+1

    def display_top_five_heroes(self, server, bot_username, phone_address):
        msg = ''
        msg += self.battle_tag + ' (Quick Play)\n-----------------------------\n'

        for h, t in zip(self.top_heroes, self.top_hours):
            msg += (h + ' - ' + t + '\n')

        server.sendmail(bot_username, phone_address, msg[:-1].encode("utf-8"))

    def display_ranked_top_five_heroes(self, server, bot_username, phone_address):
        msg = ''
        msg += self.battle_tag + ' (Competitive)\n-----------------------------\n'

        for h, t in zip(self.ranked_top_heroes, self.ranked_top_hours):
            msg += (h + ' - ' + t + '\n')

        server.sendmail(bot_username, phone_address, msg[:-1].encode("utf-8"))

    def display_quick_info(self, server, bot_username, phone_address):
        msg = ''
        msg += self.battle_tag + ' (Quick Play)\n'
        msg += '-----------------------------\n'
        msg += 'Level: ' + self.level + '\n'
        msg += 'Wins: ' + self.wins + '\n'
        msg += 'Losses: ' + self.losses + '\n'
        msg += 'Win Percentage: %.2f%%\n' % self.win_percentage
        msg += 'Time Played: ' + self.time_played + '\n'
        msg += 'Total Time Played: ' + self.total_time_played + ' hour(s)'
        server.sendmail(bot_username, phone_address, msg.encode('utf-8'))

    def display_ranked_info(self, server, bot_username, phone_address):
        msg = ''
        msg += self.battle_tag + ' (Competitive)\n'
        msg += '-----------------------------\n'
        msg += 'Skill Rating: ' + self.skill_rating + '\n'
        msg += 'Level: ' + self.level + '\n'
        msg += 'Wins: ' + self.ranked_wins + '\n'
        msg += 'Losses: ' + self.ranked_losses + '\n'
        msg += 'Win Percentage: %.2f%%\n' % self.ranked_win_percentage
        msg += 'Time Played: ' + self.ranked_time_played + '\n'
        msg += 'Total Time Played: ' + self.total_time_played + ' hour(s)'
        server.sendmail(bot_username, phone_address, msg.encode('utf-8'))
