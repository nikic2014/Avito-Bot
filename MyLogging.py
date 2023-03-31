import logging
import colorlog
#
# format = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
format = (colorlog.ColoredFormatter('%(blue)s %(levelname)s: %(name)s :%(message)s'))

class LvlFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "INFO"


bot_loger = logging.getLogger("bot_logger")
bot_loger.setLevel("DEBUG")

file_bot_handler = logging.FileHandler(f"log/bot.log", mode='w')
file_bot_handler.setFormatter(format)
file_bot_handler.setLevel("WARNING")

stream_bot_handler = colorlog.StreamHandler()
stream_bot_handler.setLevel("DEBUG")
stream_bot_handler.setFormatter(format)
bot_lvl_filter = LvlFilter()
stream_bot_handler.addFilter(bot_lvl_filter)

bot_loger.addHandler(file_bot_handler)
bot_loger.addHandler(stream_bot_handler)

bot_loger.debug("bot loger start")
bot_loger.info("bot loger start")
bot_loger.warning("bot loger start")
bot_loger.error("bot loger start")
bot_loger.critical("bot loger start")

database_loger = logging.getLogger("database_logger")
database_loger.setLevel("DEBUG")
file_database_handler = logging.FileHandler(f"log/database.log", mode='w')

file_database_handler.setFormatter(format)
file_database_handler.setLevel("WARNING")

stream_database_handler = colorlog.StreamHandler()
stream_database_handler.setLevel("DEBUG")
stream_database_handler.setFormatter(format)
database_lvl_filter = LvlFilter()
stream_database_handler.addFilter(database_lvl_filter)

database_loger.addHandler(file_database_handler)
database_loger.addHandler(stream_database_handler)

database_loger.debug("database loger start")
database_loger.info("database loger start")
database_loger.warning("database loger start")
database_loger.error("database loger start")
database_loger.critical("database loger start")
