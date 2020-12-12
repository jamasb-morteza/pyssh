#!/usr/bin/python3

from ssh.ssh import SSH
from common.my_colors import MyColors
from dc.DC import DC


def perform_command(command, args):
    if command == 'ssh.getval':
        ssh_reader = SSH.get_instance()
        print(f" {MyColors.HEADER}{args} {MyColors.OKGREEN}{ssh_reader.get_value(args)}{MyColors.ENDC}")
        return

    elif command == 'ssh.setval':
        ssh_reader = SSH.get_instance()
        arg_parts = args.split(':')
        print("argaprts")
        print(arg_parts)
        if arg_parts[1].startswith('[') and arg_parts[1].endswith(']'):
            val = arg_parts[1].strip('][').split(',')
        else:
            val = arg_parts[1]
        ssh_reader.set_value(arg_parts[0], val)
        return

    elif command == 'ssh.apply':
        ssh_reader = SSH.get_instance()
        ssh_reader.apply_config()
        return

    elif command == 'ssh.configs':
        ssh_reader = SSH.get_instance()
        ssh_reader.print_output()
        return

    elif command == 'docker.ver':
        dc = DC.get_instance()
        if dc:
            dc.get_version()

    elif command == 'docker.build':
        dc = DC.get_instance()
        if dc:
            dc.get_build()

    elif command == 'docker.exist':
        dc = DC.get_instance()
        if dc:
            dc.is_installed()
    else:
        print(f"{MyColors.FAIL}Invalid Command{MyColors.ENDC}")
    pass


def run(command):
    try:
        data = command.split(' ')
        perform_command(data[0], " ".join(data[1:]))
    except Exception as e:
        # print(f"Invalid Command {e}")
        pass


try:
    while True:
        command = input("--> ")
        if command == 'exit':
            print("App interrupted goodbye\n\n\t ¯\_(ツ)_/¯ \n\t     _\n\t     _")
            exit(0)
        run(command)
        pass
except KeyboardInterrupt:
    print("App interrupted goodbye\n\n\t ¯\_(ツ)_/¯ \n\t     _\n\t     _")
    exit(0)
