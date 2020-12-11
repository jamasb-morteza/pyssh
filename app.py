#!/usr/bin/python3

from ssh.ssh import SSH
from common.my_colors import MyColors

def perform_command(command, args):
    ssh_reader = SSH.get_instance()
    if command == 'getval':
        print(f" {MyColors.HEADER}{args} {MyColors.OKGREEN}{ssh_reader.get_value(args)}{MyColors.ENDC}")
        return

    if command == 'setval':
        arg_parts = args.split(':')

        if arg_parts[1].startswith('[') and arg_parts[1].endswith(']'):
            val = arg_parts[1].strip('][').split(',')
        else:
            val = arg_parts[1]

        ssh_reader.set_value(arg_parts[0], val)
        return

    if command == 'apply':
        ssh_reader.apply_config()
        return

    if command == 'configs':
        ssh_reader.print_output()
        return

    pass


def run(command):
    try:
        data = command.split(' ')
        perform_command(data[0], " ".join(data[1:]))
    except Exception as e:
        print(f"Invalid Command {e}")
    pass


try:
    while True:
        command = input("--> ")
        if command == 'exit':
            print("\n Good Bye \n")
            exit(0)
        run(command)
        pass
except KeyboardInterrupt:
    print("App interrupted goodbye\n\n\t ¯\_(ツ)_/¯ \n\t     _\n\t     _")
