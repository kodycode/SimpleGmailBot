import smtplib
import imaplib
import email
import time

import config
from modules.owstats import OWStats
from modules.lolrank import LOLRank

def on_listen():
    listen = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
    listen.login(config.bot_username, config.bot_password)

    return listen
    
def on_login():
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)
    server.sendmail(config.bot_username, config.phone_address, 'Kodybot ON')
    print('Gmail Bot Online')
    server.quit()

def on_message(listen):
    while (1):
        command = ''
        listen.select(mailbox="Texts")
        typ, data = listen.search(None, 'UNSEEN', 'FROM', config.phone_address)
        for num in data[0].split():
            typ, data = listen.fetch(num, '(RFC822)')
            body = email.message_from_bytes(data[0][1])
            for message in body.get_payload():
                command = str(message)[143:].replace('\n','')
                print(command)
        if (command.startswith('!logout')):
            logout()
            break;
        else:
            process_commands(command)

def on_exit(listen):
    listen.close()
    listen.logout()

def logout():
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)

    server.sendmail(config.bot_username, config.phone_address, 'Kodybot OFF')
    server.quit()
        
def process_commands(command):                
        server = smtplib.SMTP('smtp.gmail.com', port=587)
        server.starttls()
        server.login(config.bot_username, config.bot_password)
        
        if (command.startswith('!ow rtopfive')):
            battle_tag = command[13:].replace('#','-')
            
            try:
                top_five = OWStats(battle_tag)
                top_five.get_ranked_top_five_heroes()
                top_five.get_ranked_top_five_heroes_hours()
                top_five.display_ranked_top_five_heroes(server, config.bot_username, config.phone_address)
            except:
                server.sendmail(config.bot_username, config.phone_address, 'ERROR! Could not find battle tag. ' +
                                'Please check if spelling is correct for the given battle tag. Note that the battle ' +
                                'tag is case-sensitive.')
            
        elif (command.startswith('!ow topfive')):
            battle_tag = command[12:].replace('#','-')
            
            try:
                top_five = OWStats(battle_tag)
                top_five.get_top_five_heroes()
                top_five.get_top_five_heroes_hours()
                top_five.display_top_five_heroes(server, config.bot_username, config.phone_address)
            except:
                server.sendmail(config.bot_username, config.phone_address, 'ERROR! Could not find battle tag. ' +
                                'Please check if spelling is correct for the given battle tag. Note that the battle ' +
                                'tag is case-sensitive.')
            
        elif (command.startswith('!ow competitive')):
            battle_tag = command[16:].replace('#','-')

            try:
                competitive = OWStats(battle_tag)
                competitive.get_skill_rating()
                competitive.get_level()
                competitive.get_ranked_wins()
                competitive.get_ranked_losses()
                competitive.get_ranked_win_percentage()
                competitive.get_ranked_time_played()
                competitive.get_total_time_played()
                competitive.display_ranked_info(server, config.bot_username, config.phone_address)
            except:
                server.sendmail(config.bot_username, config.phone_address, 'ERROR! Could not find battle tag. ' +
                                'Please check if spelling is correct for the given battle tag. Note that the battle ' +
                                'tag is case-sensitive.')
            
        elif (command.startswith('!ow quick')):
            battle_tag = command[10:].replace('#','-')

            try:
                quick = OWStats(battle_tag)
                quick.get_level()
                quick.get_wins()
                quick.get_losses()
                quick.get_win_percentage()
                quick.get_time_played()
                quick.get_total_time_played()
                quick.display_quick_info(server, config.bot_username, config.phone_address)
            except:
                server.sendmail(config.bot_username, config.phone_address, 'ERROR! Could not find battle tag. ' +
                                'Please check if spelling is correct for the given battle tag. Note that the battle ' +
                                'tag is case-sensitive.')
            
        elif (command.startswith('!rank')):
            summoner_name = command[6:]
        
            try:
                rank = LOLRank(config.api_key, config.region, summoner_name)
                rank.get_ranked_data()
                rank.summoner = summoner_name
            
                rank.display_ranked_data(server, config.bot_username, config.phone_address)
            except KeyError:
                server.sendmail(config.bot_username, config.phone_address, 'ERROR! No ranked stats found for this player. Please ' +
                                'check if you have the correct spelling of the player and a valid API key.')

        #On hold for now

        #elif (command.startswith('!send')):
        #    target_number = command.split(' ', 2)[1]
        #    message = command.split(' ', 2)[2]
 
        #    send = Twilio(config.twilio_sid, config.twilio_auth, target_number, message)
        #    send.lookup()
        #    send.send(server, config.bot_username) 
                
        elif (command != ''):
            server.sendmail(config.bot_username, config.phone_address, 'Invalid command?')
            
        server.quit()
        time.sleep(5)

def main():
    listen = on_listen()
    on_login()
    on_message(listen)
    on_exit(listen)

main()
