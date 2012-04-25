from random import choice as rnd

class Choice(object):

    def choice(self, message):
        message = ' '.join(message)
        message = message.split(',')
        choice = rnd(message)
        return choice