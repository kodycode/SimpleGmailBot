import smtplib
import imaplib
import email
import time

import config
from modules.owstats import OWStats

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

            top_five = OWStats(battle_tag)
            top_five.get_ranked_top_five_heroes()
            top_five.get_ranked_top_five_heroes_hours()
            top_five.display_ranked_top_five_heroes(server, config.bot_username, config.phone_address)
            server.quit()
            time.sleep(5)
            
        elif (command.startswith('!ow topfive')):
            battle_tag = command[12:].replace('#','-')

            top_five = OWStats(battle_tag)
            top_five.get_top_five_heroes()
            top_five.get_top_five_heroes_hours()
            top_five.display_top_five_heroes(server, config.bot_username, config.phone_address)
            server.quit()
            time.sleep(5)
            
        elif (command.startswith('!ow competitive')):
            battle_tag = command[16:].replace('#','-')

            competitive = OWStats(battle_tag)
            competitive.get_skill_rating()
            competitive.get_level()
            competitive.get_ranked_wins()
            competitive.get_ranked_losses()
            competitive.get_ranked_win_percentage()
            competitive.get_ranked_time_played()
            competitive.get_total_time_played()
            competitive.display_ranked_info(server, config.bot_username, config.phone_address)
            server.quit()
            time.sleep(5)
            
        elif (command.startswith('!ow quick')):
            battle_tag = command[10:].replace('#','-')

            quick = OWStats(battle_tag)
            quick.get_level()
            quick.get_wins()
            quick.get_losses()
            quick.get_win_percentage()
            quick.get_time_played()
            quick.get_total_time_played()
            quick.display_quick_info(server, config.bot_username, config.phone_address)
            server.quit()
            time.sleep(5)
        elif (command != ''):
            server.sendmail(config.bot_username, config.phone_address, 'Invalid command?')
            server.quit()
            time.sleep(5)
        else:
            server.quit()
            time.sleep(5)
        

def main():
    listen = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)
    listen.login(config.bot_username, config.bot_password)
    print('Gmail Bot Online')
    server.sendmail(config.bot_username, config.phone_address, 'Kodybot ON')
    server.quit()

    on_message(listen)
    listen.close()
    listen.logout()

main()
