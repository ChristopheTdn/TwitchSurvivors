

from tbot.tbot import TBoT


if __name__ == '__main__':       
    bot = TBoT()
    bot.load_module("tbot.tbot_client")
    bot.run()