
import os
import config

#   CONSTANTS

# Check whether the specified log path exists or not

def open_log():
    if not os.path.exists(config.LOG_PATH):
        # Create a new directory because it does not exist
        os.makedirs(config.LOG_PATH)
    if not os.path.exists(config.LOG_PATH + config.LOG_FILENAME):
        # Create a new logfile if it doesn't exist
        log_file = open(config.LOG_PATH + config.LOG_FILENAME, "w")
    else:
        log_file = open(config.LOG_PATH + config.LOG_FILENAME, "a")
    return(log_file)


def send_log(message):
    log = open_log()
    log.write(message)
    log.close()
    return
