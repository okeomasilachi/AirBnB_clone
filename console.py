#!/usr/bin/python3


"""Module that defines the HBNBCommand class for handling commands."""


import cmd
import json
import re
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# Regex patterns
uuid_pattern = (r"\b[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-"
                r"[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\b")
dictionary_pattern = r"\{.*\}"
class_name_pattern = r'(.+?)\.update'
pt1 = r'\.show\("'  # <class name>.show(<id>)
pt2 = r'\.destroy\("'  # <class name>.destroy(<id>)
pt3 = r'\.update\("'
# <class name>.update(<id>, <attribute name>, <attribute value>)

# Inbuilt Models
Models = ["BaseModel", "User", "State", "City",
          "Amenity", "Place", "Review"]


def update_line_check(line):
    """
    checks condition for update features

    Args:
        line: string representation of command

    Returns:
        Bool: True if conditions passes else False
    """
    if line[-2:] == '")' or line[-1] == ")" and \
            line[-2].isnumeric() or line[-1] == ")":
        return True
    else:
        return False


def update_line_dict_check(line):
    """
    checks condition for update features for dictionaries

    Args:
        line: string representation of command

    Returns:
        Bool: True if conditions passes else False
    """
    if re.search(dictionary_pattern, line):
        return True
    else:
        return False


def update_to_dict(line):
    """
    handles parsing of command from commandline
    for updating with dictionary

    Args:
        line: string representation of command

    Returns:
        Tuple: class name, uuid, dictionary
    """
    uuid_match = re.search(uuid_pattern, line)
    dictionary_match = re.search(dictionary_pattern, line)
    class_name_match = re.search(class_name_pattern, line)

    cls_name = class_name_match.group()
    cls_name = cls_name[:-7]

    uuid = uuid_match.group()

    d = dictionary_match.group()
    d = d.replace("'", '"')
    d = json.loads(d)

    return cls_name, uuid, d


def check_all_conditions(line):
    """
    checks condition for .show, .destroy and .update features

    Args:
        line: string representation of command

    Returns:
        Bool: True if conditions passes else False
    """
    if re.finditer(f'{pt1}|{pt2}|{pt3}', line) and \
            line[-2:] == '")' or re.finditer(r'\d\)$', line[-2]):
        return True
    else:
        return False


class HBNBCommand(cmd.Cmd):
    """The HBNBCommand class is a subclass of the cmd.Cmd class in Python.

        This class provides a command-line interface for interacting with the
        application. It includes methods for various commands like create,
        show, destroy, update, etc.

        Attributes:
            prompt (str): The prompt to display in the command-line interface.

        Methods:
            do_quit(line): Quit command to exit the program.
            do_EOF(line): Exit the program when EOF is reached (Ctrl+D).
            emptyline(): Override the default behavior of emptyline.
            do_create(line): Creates a new instance of a class based on the
                input argument.
            help_create(): Provides assistance or guidance in
                creating something.
            do_show(line): Display information about an instance.
            help_show(): Display information about the show command.
            do_destroy(line): Deletes an instance based on the id
                and class name.
            help_destroy(): Display information about the destroy command.
            do_all(line): Prints all instances of a class.
            help_all(): Display help text for the command all().
            do_update(line): Performs an update operation on an
                instance's attributes.
            help_update(): Display help text for the command update().
            default(line): Handles custom commands.
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
        """Override the default behavior of emptyline.
        """
        pass

    def do_create(self, line):
        """Creates a new instance of a class based on the input argument.

        Args:
           line (str): The input command string.

        If the class name is missing, it prints '** class name missing **'.

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
        """Display information about an instance.

        Args:
            line (str): The input command string.

        If the class name or instance id is missing, it prints
        the appropriate message.
        """
        args = line.split()
        lth = len(args)
        if lth < 1:
            print("** class name missing **")
            return
        elif lth < 2:
            print("** instance id missing **")
            return
        class_name = False
        try:
            instance = storage.all()
            for i, k in instance.items():
                if k["__class__"] == args[0]:
                    class_name = True
                    if k["id"] == args[1]:
                        print(k)
                        return
        except Exception:
            pass
        finally:
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
        """Deletes an instance based on the id and class name.

        Args:
            line (str): The input command string.

        If the class name or instance id is missing, it prints the
        appropriate message.
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
                    break

        if instance_id and class_name:
            try:
                del instance[f"{args[0]}.{args[1]}"]
                with open("models/engine/instances.json", "w",
                          encoding="utf-8") as file:
                    json.dump(instance, file)
                storage.reload()
            except Exception:
                pass
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
        """Prints all instances of a class.

        Args:
            line (str): The input command string.

        If the class name is missing or the class doesn't exist,
        it prints the appropriate message.
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
        """Performs an update operation on an instance's attributes.

        Args:
            line (str): The input command string.

        If the class name, instance id, attribute name,
        or value is missing, it prints the appropriate message.
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
        """Handles custom commands.
        """
        try:
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
            elif check_all_conditions(line):
                call = True
                match = re.finditer(f'{pt1}|{pt2}|{pt3}', line)
                for mat in match:
                    if mat.group() == '.destroy("':
                        call = False
                        st_idx = line.find('.destroy("')
                        if line[-2:] == '")':
                            command = (f"{line[:st_idx]} "
                                       f"{line[st_idx + 10:-2]}")
                            self.do_destroy(command)
                        else:
                            super().default(line)
                    elif mat.group() == '.show("':
                        call = False
                        st_idx = line.find('.show("')
                        if line[-2:] == '")':
                            command = (f"{line[:st_idx]} "
                                       f"{line[st_idx + 7:-2]}")
                            self.do_show(command)
                        else:
                            super().default(line)
                    elif mat.group() == '.update("':
                        call = False
                        if update_line_dict_check(line):
                            cls_name, u_id, dic = update_to_dict(line)
                            for key, value in dic.items():
                                command = (f"{cls_name} {u_id} "
                                           f"{key} {value}")
                                self.do_update(command)
                        elif update_line_check(line):
                            my_list = []
                            split_text = re.split(r'[\s, ", \, \), \(]',
                                                  line)
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
                                            command += \
                                                f" {attribute_value}"
                                            self.do_update(command)
                                        else:
                                            self.do_update(command)
                                    else:
                                        self.do_update(command)
                                else:
                                    self.do_update(command)
                            else:
                                pass
                        else:
                            super().default(line)
                if call:
                    super().default(line)
            else:
                super().default(line)
        except IndexError as e:
            super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
