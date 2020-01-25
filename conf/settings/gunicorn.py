"""Gunicorn configuration"""
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
bind = "0.0.0.0:8000"
loglevel = 'info'

# TODO:
# * logging
