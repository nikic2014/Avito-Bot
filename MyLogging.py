import logging

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

database_loger = logging.getLogger("database_logger")
database_handler = logging.FileHandler(f"log/database.log", mode='w')
database_handler.setFormatter(formatter)
database_loger.addHandler(database_handler)


class LvlFilter(logging.Filter):
    def filter(self, record):
        print(record.levelname)
        return record.levelname == "INFO"



bot_loger = logging.getLogger("bot_logger")

file_bot_handler = logging.FileHandler(f"log/bot.log", mode='w')
file_bot_handler.setFormatter(formatter)

stream_bot_handler = logging.StreamHandler()
stream_bot_handler.setFormatter(formatter)
bot_lvl_filter = LvlFilter()
stream_bot_handler.addFilter(bot_lvl_filter)


bot_loger.addHandler(file_bot_handler)
bot_loger.addHandler(stream_bot_handler)


bot_loger.info("Hello")
bot_loger.warning("Hellow")