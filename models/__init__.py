#!/usr/bin/python3

""" Module creates an instance of the FileStorage class"""


from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
