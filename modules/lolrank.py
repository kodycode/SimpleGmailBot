import requests

class LOLRank:
    def __init__(self, api_key, region, summoner_name):
        self.summoner = summoner_name.replace(' ', '')
        self.summoner = self.summoner.lower()
        self.api_key = api_key
        self.region = region
        self.tier = ''
        self.divison = ''
        self.lp = ''
        self.wins = 0
        self.losses = 0
        self.win_percentage = 0
    
    def get_summoner_ID(self, region, summoner_name):
        URL = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + summoner_name + '?api_key=' + self.api_key
        response = requests.get(URL)
        
        return response.json()

    def request_ranked_Data(self, region, ID):
        URL = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.5/league/by-summoner/' + ID + '/entry?api_key=' + self.api_key
        response = requests.get(URL)
        
        return response.json()

    def get_ranked_data(self):

        responseJSON = self.get_summoner_ID(self.region, self.summoner, self.api_key)

        ID = responseJSON[self.summoner]['id']
        ID = str(ID)          
        responseJSON2 = self.request_ranked_Data(self.region, ID, self.api_key)

        self.tier = responseJSON2[ID][0]['tier']
        self.division = responseJSON2[ID][0]['entries'][0]['division']
        self.lp = str(responseJSON2[ID][0]['entries'][0]['leaguePoints'])
        self.wins = str(responseJSON2[ID][0]['entries'][0]['wins'])
        self.losses = str(responseJSON2[ID][0]['entries'][0]['losses'])
        self.win_percentage = (int(self.wins)/(int(self.losses) + int(self.wins))) * 100

    def display_ranked_data(self, server, bot_username, phone_address):
        server.sendmail(bot_username, phone_address, self.summoner + '\n-------------\nTier: ' + self.tier + '\nDivison: '+ self.division
                                  + '\nLP: ' + self.lp + '\nWins: ' + self.wins + '\nLosses: ' + self.losses + '\nWin Percentage: %.2f%%' % self.win_percentage)
