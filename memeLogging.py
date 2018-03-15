import logging.config
import os
import errno


# default log.conf file contents
def get_default_conf():

    conf_content = '''
[loggers]
keys=root
[logger_root]
handlers=screen,file
level=NOTSET
[formatters]
keys=simple,complex
[formatter_simple]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
[formatter_complex]
format=%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s
[handlers]
keys=file,screen
[handler_file]
class=handlers.TimedRotatingFileHandler
interval=midnight
backupCount=5
formatter=complex
level=DEBUG
args=('logs/memelog.log',)              # change this filename to whatever you want
[handler_screen]
class=StreamHandler
formatter=simple
level=INFO
args=(sys.stdout,)
'''
    return conf_content


def make_logging_folder():

# makedirs doc https://docs.python.org/3/library/os.html#os.makedirs
    log_folder = "logs"
    log_config_file = os.path.join(log_folder, "log.conf")

    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(log_folder, exist_ok=True)

        # if the log.conf file doesn't exist, create the file
        if not os.path.exists(log_config_file):
            default_conf = get_default_conf()
            with open(log_config_file, 'w') as new_conf_file:
                new_conf_file.write(default_conf)

        return log_config_file

    except OSError as e:
        print(e.errno)


def logging_setup():
    # logging setup
    # logging.debug("1")          # test logging level    these 5 lines are just examples for reference
    # logging.info("2")           # test logging level
    # logging.warning("3")        # test logging level
    # logging.error("4")          # test logging level
    # logging.critical("5")       # test logging level
    log_config_file = make_logging_folder()
    logging.config.fileConfig(log_config_file)  # contains formatting directives
