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


if __name__ == "__main__":

    pt1 = r'\.show\("'
    pt2 = r'\.destroy\("'
    pt3 = r'\.update\("'

    # The HBNBCommand class is a subclass of the cmd.Cmd class in Python.
    class HBNBCommand(cmd.Cmd):

        prompt = "(hbnb) "

        def do_quit(self, line):
            """
            quits the interpreter
            """
            exit(0)

        def help_quit(self):
            """
            explaining how to quit the program.
            """
            print('\n'.join(['Quit command to exit the program']))

        def do_EOF(self, line):
            """
            prints a new line and returns True.

            Args:
              line: String that represents the input
                line that was entered by the user.

            Returns:
              True.
            """
            print()
            return True

        def help_EOF(self):
            """
            prints a message explaining the purpose of the "EOF" command.
            """
            print('\n'.join(['Quit command to exit the program']))

        def default(self, line):
            """
            Overrides default method that handles various commands in a
            Python interactive shell, including handling ".all()",
            ".count()", ".destroy()", ".show()", and ".update()" commands.

            Args:
              line: string that represents the input command or statement that
                needs to be processed.
            """
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
            elif re.finditer(f'{pt1}|{pt2}|{pt3}', line) and \
                    line[-2:] == '")' or re.finditer(r'\d\)$', line[-2]):

                match = re.finditer(f'{pt1}|{pt2}|{pt3}', line)
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
                        my_list = []
                        split_text = re.split(r'[\s, ", \, \), \(]', line)
                        for arg in split_text:
                            if arg != '':
                                my_list.append(arg)
                        my_list[0] = my_list[0][:-7]
                        list_length = len(my_list)
                        if list_length > 0:
                            class_name = my_list[0]
                            command = class_name
                            if list_length > 1:
                                instance_id = my_list[1]
                                command += f" {instance_id}"
                                if list_length > 2:
                                    attribute_name = my_list[2]
                                    command += f" {attribute_name}"
                                    if list_length > 3:
                                        attribute_value = my_list[3]
                                        command += f" {attribute_value}"
                                        self.do_update(command)
                                    else:
                                        c_m_d = (f"{class_name} {instance_id} "
                                                 f"{attribute_name}")
                                        self.do_update(c_m_d)
                                else:
                                    command = f"{class_name} {instance_id}"
                                    self.do_update(command)
                            else:
                                command = f"{class_name}"
                                self.do_update(command)
                        else:
                            command = f"{class_name}"
                            self.do_update(command)
            else:
                super().default(line)

        def emptyline(self):
            """
            The function "emptyline" does nothing and
            serves as a placeholder.
            """
            pass

        def do_create(self, line):
            """
            creates a new instance of a class based on the input argument
            and saves it, then prints the ID of the newly created instance.

            Args:
              line: string that represents the input command.
                It is expected to contain the class name for
                creating a new instance of a class.
            """
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
            """
            provides assistance or guidance in creating something.
            """
            print('\n'.join(['create [Model]',
                             'Creates a new instance of an inbuilt Model',
                             'If the class name is missing\n\t'
                             'print ** class name missing **']))

        def do_show(self, line):
            """
            The function "do_show" is used to display information
            about and instance

            Args:
              line: The `line` parameter is a string that represents
                the user input for the command. It typically contains
                the command itself and any arguments or options that
                the user has provided.
            """
            args = line.split()
            if not args:
                print("** class name missing **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                class_name = args[0]
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
                        if value["__class__"] == class_name:
                            class_present = True
                        if value["id"] == identity and \
                                value["__class__"] == class_name:
                            class_id = True
                            print(f"[{value['__class__']}] "
                                  f"({value['id']}) {value}")
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

        def help_show(self):
            """
            display information or documentation about the
            show command
            """
            print('\n'.join(['show [Model] <id>',
                             'Prints the string representation of an instance',
                             'based on the class name and id']))

        def do_destroy(self, line):
            """
            Deletes an instance based on the id and class name.

            Args:
              line: string that represents the command or input
                provided by the user.
            """
            args = line.split()
            if not args:
                print("** class name missing **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                class_name = args[0]
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
                        if value["__class__"] == class_name:
                            class_present = True
                        if value["id"] == id and \
                                value["__class__"] == class_name:
                            class_id = True
                    if class_present and class_id:
                        del data[f"{class_name}.{id}"]
                        with open("instances.json", "w", encoding="utf-8") \
                                as file:
                            file.write(json.dumps(data))
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

        def help_destroy(self):
            """
            prints help text to STDOUT about the destroy command.
            """
            print('\n'.join(['destroy [Model] <id>',
                             'Deletes an instance',
                             'based on the class name and id']))

        def do_all(self, line):
            """
            prints all instances of a class

            Args:
              line: string that represents the input command or
                instruction that the user wants to execute.
            """
            args = line.split()
            if len(args) == 1:
                return_list = []
                class_present = False
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        if value["__class__"] == args[0]:
                            class_present = True
                            return_list.append(f"[{value['__class__']}] "
                                        f"({value['id']}) {value}")
                    if class_present:
                        print(return_list)
                    elif not class_present:
                        print("** class doesn't exist **")
                else:
                    print("** class doesn't exist **")
            elif len(line) < 1:
                return_list = []
                if os.path.exists("instances.json"):
                    with open("instances.json", "r", encoding="utf-8") as file:
                        data = file.read()
                        data = json.loads(data)
                        file.close()
                    for key, value in data.items():
                        return_list.append(f"[{value['__class__']}] "
                                    f"({value['id']}) {value}")
                    print(return_list)
            else:
                self.default(line)

        def help_all(self):
            """
            prints Help text for the command all()
            """
            print('\n'.join(['all',
                             'all [Model]',
                             'Prints all string representation of all '
                             'instances',
                             'based or not on the class name.']))

        def do_update(self, line):
            """
            performs an update operation on an instance attributes.

            Args:
              line: string that represents the input command or
                instruction that the user wants to execute.
            """
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
                        if value["id"] == args[1] and \
                                value["__class__"] == args[0]:
                            class_id = True
                            var = args[3].replace('\"', '')
                            value[args[2]] = var
                    if class_present and class_id:
                        with open("instances.json", "w", encoding="utf-8") \
                                as file:
                            file.write(json.dumps(data))
                            file.close()
                    if class_present and not class_id:
                        print("** no instance found **")
                    elif not class_present:
                        print("** class doesn't exist **")

        def help_update(self):
            """
            prints Help text for the command update()
            """
            print('\n'.join(['update',
                             'updates an instance,'
                             'based on class name, '
                             'id, attribute name and value']))

    HBNBCommand().cmdloop()
