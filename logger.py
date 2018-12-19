from datetime import datetime


def info(text):
    print('[%s] %s' % (datetime.now(), text))
