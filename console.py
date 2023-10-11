#!/usr/bin/python3

import cmd
import json
import os
from models.base_model import BaseModel as Bm

if __name__ == "__main__":

    class HBNBCommand(cmd.Cmd):

        prompt = "(hbnb) "

        def do_quit(self, line):
            """
            quit
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

        def emptyline(self):
            pass

        def do_create(self, line):
            if not line:
                print("** class name missing **")
            elif line in ["BaseModel"]:
                match line:
                    case BaseModel:
                        new = Bm()
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
                            var = args[3]
                            print(var[1:-1])
                    if class_present and class_id:
                        with open("instances.json", "w", encoding="utf-8") as file:
                            file.write(json.dumps(data))
                            file.close()

                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

    HBNBCommand().cmdloop()
