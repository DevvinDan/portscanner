from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import json


class QuestBot:

    def __init__(self, current_stage):

        # Load bot answers and other info

        with open('data.json', 'r') as f:
            bot_data = json.load(f)

        self.token = bot_data["token"]
        self.logging_id = bot_data["logging_id"]
        self.stage_messages = bot_data["stage_messages"]
        self.greetings = bot_data["greetings"]
        self.keys = bot_data["keys"]
        self.questions = bot_data["questions"]
        self.congratulations = bot_data["congratulations"]
        self.hints = bot_data["hints"]


        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        self.stage_handlers = {
            'start' : self.start_stage_handler,
            'questions' : self.questions_stage_handler,
            'pre-music': self.pre_music_stage_handler,
            'music': self.music_stage_handler,
            'video-quest': self.video_quest_stage_handler,
            'find-photos': self.find_photos_stage_handler,
            'final': self.final_stage_handler
        }

        self.current_question = {
            int(self.logging_id): 0
        }

        self.current_stage = current_stage

        start_game_handler = CommandHandler('start', self.start_game)
        hint_handler = CommandHandler('hint', self.give_hint)
        message_handler = MessageHandler(Filters.text, self.message_handler)

        self.dispatcher.add_handler(start_game_handler)
        self.dispatcher.add_handler(hint_handler)
        self.dispatcher.add_handler(message_handler)

    def log(self, bot, update, comment=""):
        try:
            name = update.message.from_user.first_name
            text = update.message.text
            date = update.message.date
            record = "[{}] {}: {}  ({})".format(date, name, text, comment)
            bot.send_message(chat_id=self.logging_id, text=record)
        except Exception as e:
            print(e)


    def start_game(self, bot, update):
        self.current_stage = 'start'
        self.log(bot, update, self.current_stage)
        self.current_question[update.message.chat_id] = 0
        bot.send_message(chat_id=update.message.chat_id, text=self.greetings[self.current_stage])

    def give_hint(self, bot, update):
        self.log(bot, update, self.current_stage)
        sender_id = update.message.chat_id
        if self.current_stage not in self.hints:
            hint = "Похоже, на этот вопрос нет подсказки."
        else:
            hint = self.hints[self.current_stage][self.current_question[sender_id]]
        bot.send_message(chat_id=sender_id, text=hint)


    def message_handler(self, bot, update):
        """Chooses the correct handler depending on running stage"""
        try:
            self.stage_handlers[self.current_stage](bot, update)
        except Exception as e:
            print(e)
            raise e



    def start_stage_handler(self, bot, update):
        """Start of the game where Kate meets the stranger"""
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage].lower() == update.message.text.lower():
            self.current_stage = 'questions'
            self.current_question[sender_id] = 0
            bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
            bot.send_message(chat_id=sender_id, text=self.questions[self.current_question[sender_id]])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def questions_stage_handler(self, bot, update):
        """The stage where bot asks 5 questions and waits until Kate answers them all"""
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage][self.current_question[sender_id]].lower() == update.message.text.lower():
            bot.send_message(chat_id=sender_id, text=self.congratulations[self.current_stage][self.current_question[sender_id]])
            self.current_question[sender_id] += 1
            if self.current_question[sender_id] > 4:
                self.current_stage = 'pre-music'
                try:
                    bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
                except Exception as e:
                    print(e)
            else:
                bot.send_message(chat_id=sender_id, text=self.questions[self.current_question[sender_id]])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def pre_music_stage_handler(self, bot, update):
        """Sends Kate to find music player somewhere to 16'th floor"""
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage].lower() == update.message.text.lower():
            self.current_stage = 'music'
            self.current_question[sender_id] = 0
            bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def music_stage_handler(self, bot, update):
        """Kate listens to the music and guesses song's names"""
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage][self.current_question[sender_id]].lower() == update.message.text.lower():
            bot.send_message(chat_id=sender_id, text=self.congratulations[self.current_stage][self.current_question[sender_id]])
            self.current_question[sender_id] += 1
            if self.current_question[sender_id] > 9:
                self.current_question[sender_id] = 0
                self.current_stage = 'video-quest'
                bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def video_quest_stage_handler(self, bot, update):
        """Kate completes video quest and enters secret code"""
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage].lower() == update.message.text.lower():
            self.current_stage = "find-photos"
            bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def find_photos_stage_handler(self, bot, update):
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage].lower() == update.message.text.lower():
            self.current_stage = "final"
            bot.send_message(chat_id=sender_id, text=self.greetings[self.current_stage])
        else:
            bot.send_message(chat_id=sender_id, text=self.stage_messages[self.current_stage])

    def final_stage_handler(self, bot, update):
        sender_id = update.message.chat_id
        self.log(bot, update, self.current_stage)
        if self.keys[self.current_stage].lower() == update.message.text.lower():
            bot.send_message(chat_id=sender_id, text=self.greetings["last-message"])


bot = QuestBot('music')
bot.updater.start_polling()