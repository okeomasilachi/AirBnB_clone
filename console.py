#!/usr/bin/python3


import cmd
import json
import os
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

pt1 = r'\.show\("'
pt2 = r'\.destroy\("'
pt3 = r'\.update\("'

if __name__ == "__main__":

    class HBNBCommand(cmd.Cmd):

        prompt = "(hbnb) "

        def do_quit(self, line):
            """
            quits the interpreter
            """
            exit(0)

        def help_quit(self):
            print('\n'.join(['Quit command to exit the program']))

        def do_EOF(self, line):
            print()
            return True

        def help_EOF(self):
            print('\n'.join(['Quit command to exit the program']))


        def default(self, line):
            if (st_idx := line.find(".all()")) != -1:
                self.do_all(line[:st_idx])
            elif (st_idx := line.find(".count()")) != -1:
                i = 0
                class_present = False
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == line[:st_idx]:
                            class_present = True
                            i += 1
                    if class_present:
                        print(i)
                        i = 0
                    elif not class_present:
                        print("** class doesn't exist **")
            elif re.finditer(f'{pt1}|{pt2}|{pt3}', line) and line[-2:] == '")':
                match = re.finditer(f'{pt1}|{pt2}', line)
                for mat in match:
                    if mat.group() == '.destroy("':
                        st_idx = line.find('.destroy("')
                        command = f"{line[:st_idx]} {line[st_idx + 10:-2]}"
                        self.do_destroy(command)
                    elif mat.group() == '.show("':
                        st_idx = line.find('.show("')
                        command = f"{line[:st_idx]} {line[st_idx + 7:-2]}"
                        self.do_show(command)
                    elif mat.group() == '.update("':
                        print("update")
            else:
                super().default(line)

        def emptyline(self):
            pass

        def do_create(self, line):
            args = line.split()
            if not args:
                print("** class name missing **")
            elif args[0] in ["BaseModel", "User", "State", "City",
                             "Amenity", "Place", "Review"]:
                match args[0]:
                    case "BaseModel":
                        new = BaseModel()
                        new.save()
                        print(new.id)
                    case "User":
                        new = User()
                        new.save()
                        print(new.id)
                    case "State":
                        new = State()
                        new.save()
                        print(new.id)
                    case "City":
                        new = City()
                        new.save()
                        print(new.id)
                    case "Amenity":
                        new = Amenity()
                        new.save()
                        print(new.id)
                    case "Place":
                        new = Place()
                        new.save()
                        print(new.id)
                    case "Review":
                        new = Review()
                        new.save()
                        print(new.id)
            else:
                print("** class doesn't exist **")

        def help_create(self):
            print('\n'.join(['create [Model]',
                             'Creates a new instance of an inbuilt Model',
                             'If the class name is missing\n\t'
                             'print ** class name missing **']))

        def do_show(self, line):
            args = line.split()
            if not args:
                print("** class name missing **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                classname = args[0]
                identity = args[1]
                data = None
                class_present = False
                class_id = False
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == classname:
                            class_present = True
                        if value["id"] == identity and value["__class__"] == classname:
                            class_id = True
                            print(f"[{value['__class__']}] "
                                  f"({value['id']}) {value}")
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

        def help_show(self):
            print('\n'.join(['show [Model] <id>',
                             'Prints the string representation of an instance',
                             'based on the class name and id']))

        def do_destroy(self, line):
            args = line.split()
            if not args:
                print("** class name missing **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                classname = args[0]
                id = args[1]
                data = None
                class_present = False
                class_id = False
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == classname:
                            class_present = True
                        if value["id"] == id and value["__class__"] == classname:
                            class_id = True
                    if class_present and class_id:
                        del data[f"{classname}.{id}"]
                        with open("instances.json", "w", encoding="utf-8") as file:
                            file.write(json.dumps(data))
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

        def help_destroy(self):
            print('\n'.join(['destroy [Model] <id>',
                             'Deletes an instance',
                             'based on the class name and id']))

        def do_all(self, line):
            args = line.split()
            if len(args) == 1:
                list = []
                class_present = False
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == args[0]:
                            class_present = True
                            list.append(f"[{value['__class__']}] "
                                        f"({value['id']}) {value}")
                    if class_present:
                        print(list)
                    elif not class_present:
                        print("** class doesn't exist **")
                else:
                    print("** class doesn't exist **")
            elif len(line) < 1:
                list = []
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        list.append(f"[{value['__class__']}] "
                                    f"({value['id']}) {value}")
                    print(list)
            else:
                self.default(line)

        def help_all(self):
            print('\n'.join(['all',
                             'all [Model]',
                             'Prints all string representation of all instances',
                             'based or not on the class name.']))

        def do_update(self, line):
            args = line.split()
            data = None
            class_present = False
            class_id = False
            match len(args):
                case 3:
                    print("** value missing **")
                case 2:
                    print("** attribute name missing **")
                case 1:
                    print("** instance id missing **")
                case 0:
                    print("** class name missing **")
            if len(args) >= 4:
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == args[0]:
                            class_present = True
                        if value["id"] == args[1] and value["__class__"] == args[0]:
                            class_id = True
                            var = args[3].replace('\"', '')
                            value[args[2]] = var
                    if class_present and class_id:
                        with open("instances.json", "w", encoding="utf-8") as file:
                            file.write(json.dumps(data))
                            file.close()
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

    HBNBCommand().cmdloop()
