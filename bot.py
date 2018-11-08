import smtplib
import imaplib
import email
import time
import config


def on_listen():
    listen = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
    listen.login(config.bot_username, config.bot_password)
    return listen


def on_login():
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)
    server.sendmail(config.bot_username, config.phone_address, 'GmailBot ON')
    print('Gmail Bot Online')
    server.quit()


def on_message(listen):
    while (1):
        command = ''
        listen.select(mailbox="Inbox")
        typ, data = listen.search(None, 'UNSEEN', 'FROM', config.phone_address)
        for num in data[0].split():
            typ, data = listen.fetch(num, '(RFC822)')
            body = email.message_from_bytes(data[0][1])
            for message in body.get_payload():
                command = str(message)[143:].replace('\n', '')
                print(command)
        if (command.startswith('!logout')):
            logout()
            break
        else:
            process_commands(command)


def on_exit(listen):
    listen.close()
    listen.logout()


def logout():
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)

    server.sendmail(config.bot_username, config.phone_address, 'GmailBot OFF')
    server.quit()


def process_commands(command):
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(config.bot_username, config.bot_password)

    if (command != ''):
        server.sendmail(config.bot_username, config.phone_address, 'Invalid command?')

    server.quit()
    time.sleep(5)


def main():
    listen = on_listen()
    on_login()
    on_message(listen)
    on_exit(listen)


main()
