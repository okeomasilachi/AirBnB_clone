#!/usr/bin/python3


""" Model holds the class HBNBCommand """

import cmd
import json
import os
import re
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """
    The HBNBCommand class is a subclass of the cmd.Cmd class in Python.
    """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """Exit the program when EOF is reached (Ctrl+D)
        """
        return True

    def emptyline(self):
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
        if not line:
            print("** class name missing **")
            return

        try:
            new_instance = eval(line.split()[0])()
            new_instance.save()
            print(new_instance.id)
        except Exception:
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
        lth = len(args)
        if lth < 1:
            print("** class name missing **")
            return
        elif lth < 2:
            print("** instance id missing **")
            return

        instance = storage.all()
        class_name = False
        for i, k in instance.items():
            if k["__class__"] == args[0]:
                class_name = True
                if k["id"] == args[1]:
                    print(k)
                    return
        if class_name:
            print("** no instance found **")
        else:
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
        lth = len(args)
        if lth < 1:
            print("** class name missing **")
            return
        elif lth < 2:
            print("** instance id missing **")
            return

        instance = storage.all()
        class_name = False
        instance_id = False
        for i, k in instance.items():
            if k["__class__"] == args[0]:
                class_name = True
                if k["id"] == args[1]:
                    instance_id = True

        if instance_id and class_name:
            del instance[f"{args[0]}.{args[1]}"]
            storage.set_all(instance)
            storage.save()
        elif class_name:
            print("** no instance found **")
        else:
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
            class_present = False
            for key, value in storage.all().items():
                if value["__class__"] == args[0]:
                    class_present = True
            if class_present:
                print([f"[{value['__class__']}] ({value['id']}) {value}"
                       for value in storage.all().values()
                       if value["__class__"] == args[0]])
            elif not class_present:
                print("** class doesn't exist **")
        elif len(line) < 1:
            print([f"[{value['__class__']}] ({value['id']}) {value}"
                   for value in storage.all().values()])
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
        length = len(args)
        if length == 3:
            print("** value missing **")
            return
        elif length == 2:
            print("** attribute name missing **")
            return
        elif length == 1:
            print("** instance id missing **")
            return
        elif length == 0:
            print("** class name missing **")
        if len(args) >= 4:
            instance = storage.all()
            class_name = False
            instance_id = False
            for i, k in instance.items():
                if k["__class__"] == args[0]:
                    class_name = True
                    if k["id"] == args[1]:
                        instance_id = True

            if instance_id and class_name:
                try:
                    old = instance[f"{args[0]}.{args[1]}"]
                    value = args[3]
                    value = value.replace('"', '')
                    if value.isdigit():
                        if float(value).is_integer():
                            value = int(float(value))
                        else:
                            value = float(value)
                    old[args[2]] = value
                    new_instance = eval(args[0])(**old)
                    storage.new(new_instance)
                    return
                except Exception:
                    pass
            if class_name and not instance_id:
                print("** no instance found **")
                return
            elif not class_name:
                print("** class doesn't exist **")

    def help_update(self):
        """
        prints Help text for the command update()
        """
        print('\n'.join(['update',
                         'updates an instance,'
                         'based on class name, '
                         'id, attribute name and value']))

    def default(self, line):
        if line.find(".all()") != -1:
            st_idx = line.find(".all()")
            self.do_all(line[:st_idx])
        elif line.find(".count()") != -1:
            st_idx = line.find(".count()")
            i = 0
            class_present = False
            for key, value in storage.all().items():
                if value["__class__"] == line[:st_idx]:
                    class_present = True
                    i += 1
            if class_present:
                print(i)
            elif not class_present:
                print("** class doesn't exist **")
        else:
            super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
