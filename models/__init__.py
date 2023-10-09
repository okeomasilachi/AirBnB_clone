#!/usr/bin/python3

""" Module creates an instance of the FileStorage class"""


from .engine import file_storage


storage = file_storage.FileStorage()
storage.reload()
