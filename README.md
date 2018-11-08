# GmailBot
Simple Gmail Bot

It relays messages to and from a phone number and to the email address based on the specified contents in `config.py`. Basic functionality of the bot includes telling the phone number that the gmail bot is online, and can respond with `Pong!` upon texting a message to the gmail account with `!ping`.

As a note when filling out config.py, `phone_address` is specified because phone numbers are similarly email addresses. Not only do you need to supply a phone number, but also the email extension of the number based on your mobile service provider. For example, if you had verizon it'd be `1234567890@vtext.com`, where the numbers are arbitrary and represent your specified phone number to send messages to.

Intended for educational purposes only.
