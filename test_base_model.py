#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User
import cmd

"""
my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

print("--")
print()
print()
print("--")
my_new_model = BaseModel(**my_model_json)
print(my_new_model.id)
print(my_new_model)
print(type(my_new_model.created_at))

print("--")
print(my_model is my_new_model)
"""

"""
all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new object --")
my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
my_model.save()
print(my_model)
"""


"""
class HBNB(cmd.Cmd):

    prompt = "HBNB: "
    def do_name(self, value):
        if value:
            print("Hi", value)
        else:
            print("Hello")

    def do_Base(self, *args, **kwargs):
        new = BaseModel(args, kwargs)
        print(new.id)

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def default(self, line):
        print("ERROR: '{}' Not a recognizes command or Syntax".format(line))


if __name__ == "__main__":
    import sys
    do = False
    app = HBNB()
    if len(sys.argv) > 1:
        do = True
        app.onecmd(' '.join(sys.argv[1:]))
    else:
        app.cmdloop()
    if not do:
        print()
"""
all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = BaseModel()
my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.first_name = "John"
my_user2.email = "airbnb2@mail.com"
my_user2.password = "root"
my_user2.save()
print(my_user2)
