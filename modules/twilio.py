from twilio.rest.lookups import TwilioLookupsClient

class Twilio:

    def __init__(self, twilio_sid, twilio_auth, target_number, message):
        self.account_sid = twilio_sid
        self.auth = twilio_auth
        self.client = TwilioLookupsClient(self.account_sid, self.auth)
        self.target_number = str(target_number)
        self.target_message = str(message)
        self.target_carrier = ''
        
    def lookup(self):
        number = self.client.phone_numbers.get(self.target_number, include_carrier_info=True)
        self.target_carrier = number.carrier['name']
        self.get_extension()

    def get_extension(self):
        if 'Verizon' in self.target_carrier:
            self.target_number += '@vtext.com'
        elif 'Alltel' in self.target_carrier:
            self.target_number += '@message.alltel.com'
        elif 'AT&T' in self.target_carrier:
            self.target_number += '@txt.att.net'
        elif 'Boost Mobile' in self.target_carrier:
            self.target_number += '@myboostmobile.com'
        elif 'Spring' in self.target_carrier:
            self.target_number += '@messaging.sprintpcs.com'
        elif 'T-Mobile' in self.target_carrier:
            self.target_number += '@tmomail.net'
        elif 'US Cellular' in self.target_carrier:
            self.target_number += '@email.uscc.net'
        elif 'Virgin Mobile' in self.target_carrier:
            self.target_number += '@vmobl.com'
        elif 'Metro PCS' in self.target_carrier:
            self.target_number += '@mymetropcs.com'

    def send(self, server, bot_username):
        server.sendmail(bot_username, self.target_number, self.target_message)
        
