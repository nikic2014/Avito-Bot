import logging

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

database_loger = logging.getLogger("database_logger")
database_handler = logging.FileHandler(f"log/database.log", mode='w')
database_handler.setFormatter(formatter)
database_loger.addHandler(database_handler)


class LvlFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "INFO"


bot_loger = logging.getLogger("bot_logger")
bot_loger.setLevel("DEBUG")

file_bot_handler = logging.FileHandler(f"log/bot.log", mode='w')
file_bot_handler.setFormatter(formatter)
file_bot_handler.setLevel("WARNING")

stream_bot_handler = logging.StreamHandler()
stream_bot_handler.setLevel("DEBUG")
stream_bot_handler.setFormatter(formatter)
bot_lvl_filter = LvlFilter()
stream_bot_handler.addFilter(bot_lvl_filter)

bot_loger.addHandler(file_bot_handler)
bot_loger.addHandler(stream_bot_handler)

bot_loger.debug("1")
bot_loger.info("2")
bot_loger.warning("3")
bot_loger.error("4")
bot_loger.critical("5")
