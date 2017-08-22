#!/usr/local/python3
import os

os.environ['USER_SETTINGS'] = "config.settings"
from src import script
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

if __name__ == '__main__':
    script.run()
