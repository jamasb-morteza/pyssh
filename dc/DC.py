import os
from common.my_colors import MyColors


class DC:
    __line = ''
    __data = None
    __instance = None

    def __init__(self):
        f = os.popen("docker -v")
        self.__line = f.read()
        self.__data = self.parse_data()

    def get_version(self):
        if not self.__data:
            return None
        print(f"{MyColors.HEADER}Version is: {MyColors.OKGREEN}{self.__data['version']}{MyColors.ENDC}")
        pass

    def get_build(self):
        if not self.__data:
            print(f"{MyColors.WARNING}Docker is Not installed{MyColors.ENDC}")
        print(f"{MyColors.HEADER}Build is: {MyColors.OKGREEN}{self.__data['build']}{MyColors.ENDC}")
        pass

    def is_installed(self):
        if not self.__data:
            print(f"{MyColors.WARNING}Docker is Not installed{MyColors.ENDC}")
        else:
            print(f"{MyColors.OKGREEN}Docker is installed{MyColors.ENDC}")

    def parse_data(self):
        if self.__line.find("Docker") == -1:
            return None
        line_data = self.__line.split(',')
        try:
            return {
                'version': line_data[0].strip().split(' ')[2],
                'build': line_data[1].strip().split(' ')[1]
            }
        except Exception:
            print(f"can't get docker info: {Exception}")

        return None
    @staticmethod
    def get_instance():
        if not DC.__instance:
            try:
                DC.__instance = DC()
            except FileNotFoundError as exception:
                print(f"{exception}")
                return None
        return DC.__instance
