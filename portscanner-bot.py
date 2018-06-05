from telegram.ext import Updater
from telegram.ext import CommandHandler
from datetime import datetime
import json
import portscanner as ps
import os
import time

class ScannerBot:

    def __init__(self):

        # Load bot answers and other info

        with open('data.json', 'r') as f:
            bot_config = json.load(f)

        self.token = str(os.getenv('TOKEN'))
        self.app_port = int(os.getenv('PORT', '8443'))

        self.replies = bot_config['replies']['eng']
        self.scanning_template = self.replies['scanning_template']
        self.scanning_completed_template = self.replies['scanning_completed_template']
        self.start_scanning_template = self.replies['start_scanning_template']

        self.MAX_MESSAGE_SIZE = 4096


        # Creating Bot core
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher
        self.scanner = ps.PortScanner()
        self.ip_range = []
        self.port_range = []


        #Adding handlers

        start_handler = CommandHandler('start', self.start)
        help_handler = CommandHandler('help', self.help)
        set_port_handler = CommandHandler('set_port', self.set_port, pass_args=True)
        set_ip_handler = CommandHandler('set_ip', self.set_ip, pass_args=True)
        scan_handler = CommandHandler('scan', self.scan)
        set_timeout_handler = CommandHandler('settimeout', self.set_timeout, pass_args=True)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(set_port_handler)
        self.dispatcher.add_handler(set_ip_handler)
        self.dispatcher.add_handler(scan_handler)
        self.dispatcher.add_handler(set_timeout_handler)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.replies['start'])

    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.replies['help'])

    def set_port(self, bot, update, args):
        try:
            input = ' '.join(args)
            self.port_range = list(self.scanner.get_port_range(input))
            bot.send_message(chat_id=update.message.chat_id, text="Port set to {}".format(input))
        except:
            self.port_range = []
            bot.send_message(chat_id=update.message.chat_id, text=self.replies['exception_input'])

    def set_ip(self, bot, update, args):
        try:
            input = ' '.join(args)
            self.ip_range = list(self.scanner.get_ip_range(input))
            bot.send_message(chat_id=update.message.chat_id, text="IP set to {}".format(input))
        except:
            self.ip_range = []
            bot.send_message(chat_id=update.message.chat_id, text=self.replies['exception_input'])

    def scan(self, bot, update):
        if len(self.ip_range) == 0 or len(self.port_range) == 0:
            bot.send_message(chat_id=update.message.chat_id, text=self.replies['exception_not_set'])
            return
        try:
            message = ""
            for ip in self.ip_range:
                start = datetime.now()
                new_chunk = self.start_scanning_template.format(ip)
                if self.check_message_size(new_chunk, message):
                    message += new_chunk
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=message)
                    message = new_chunk
                    time.sleep(1)
                for port in self.port_range:
                    result = self.scanner.scan_port(ip, port)
                    if result:
                        new_chunk = self.scanning_template.format(port, self.scanner.get_service_name(port))
                        if not self.check_message_size(message, new_chunk):
                            bot.send_message(chat_id=update.message.chat_id, text=message)
                            message = new_chunk
                            time.sleep(1)
                        else:
                            message += new_chunk
                end = datetime.now()
                totaltime = end - start
                new_chunk = self.scanning_completed_template.format(totaltime)
                if self.check_message_size(new_chunk, message):
                    message += new_chunk
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=message)
                    message = new_chunk
                    time.sleep(1)
            if len(message) > 0:
                bot.send_message(chat_id=update.message.chat_id, text=message)
                time.sleep(1)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=update.message.chat_id, text=self.replies['exception_value'])

    def check_message_size(self, message, chunk):
        if len(message) + len(chunk) <= self.MAX_MESSAGE_SIZE:
            return True
        else:
            return False

    def set_timeout(self, bot, update, args):
        input = ' '.join(args)
        try:
            self.scanner.set_timeout(float(input))
        except:
            bot.send_message(chat_id=update.message.chat_id, text=self.replies['exception_timeout'])


    def log(self, bot, update, comment=""):
        try:
            name = update.message.from_user.first_name
            text = update.message.text
            date = update.message.date
            record = "[{}] {}: {}  ({})".format(date, name, text, comment)
            print(record)
        except Exception as e:
            print(e)



bot = ScannerBot()

bot.updater.start_webhook(listen="0.0.0.0",
                      port=bot.app_port,
                      url_path=bot.token)
bot.updater.bot.set_webhook("https://portscannerbot.herokuapp.com/" + bot.token)
bot.updater.idle()