import smtplib
import imaplib
import email
import time

import config

def on_message(listen):
    command = ''
    while (1):
        listen.select(mailbox="Texts")
        typ, data = listen.search(None, 'UNSEEN', 'FROM', phone_address)
        for num in data[0].split():
            typ, data = listen.fetch(num, '(RFC822)')
            body = email.message_from_bytes(data[0][1])
            for message in body.get_payload():
                command = str(message)[143:].replace('\n','')
                print(command)
                
        if (command == '!logout'):
            break;
        else:
            time.sleep(5)

def main():
    listen = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(bot_username, bot_password)
    listen.login(bot_username, bot_password)
    server.sendmail(bot_username, phone_address, 'Kodybot ON')

    on_message(listen)
    server.sendmail(bot_username, phone_address, 'Kodybot OFF')
    listen.close()
    listen.logout()
    server.quit()

main()
