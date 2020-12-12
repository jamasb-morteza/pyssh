from common.my_colors import MyColors


class SSH:
    __instance = None
    __configs = {}
    __lines = 0
    __changed_lines = {}
    __file_path = '/etc/ssh/sshd_config_temp'

    def __init__(self, file='/etc/ssh/sshd_config_temp'):
        self.__file_path = file
        self.read_file()

    def read_file(self):
        with open(self.__file_path) as file:
            row = 0
            for line in file:
                row += 1

                line_data = self.parse_line(line.strip())
                if not line_data:
                    continue
                line_data['row'] = row
                self.__configs[line_data['key']] = line_data
            self.__lines = row

    def parse_line(self, line):
        line = line.strip()
        if line == "" or line.startswith('#'):
            return None

        line = line.strip('\t')
        if line.find('\t') != -1:
            separator = '\t'
        else:
            separator = ' '

        data = line.split(separator)
        key = data[0]
        value = data[1:] if len(data[1:]) > 1 else data[1]
        return {'key': key, 'values': value, 'separator': separator}

    def get_value(self, key):
        try:
            if key not in self.__configs:
                return "option not set"
            value = self.__configs[key]['values']
            separator = self.__configs[key]['separator']
            if isinstance(self.__configs[key]['values'], list):
                return separator.join(value)
            return value
        except:
            return None

    def set_value(self, key, val, apply=False):
        if not key in self.__configs:
            self.__lines += 1
            print(self.__lines)
            self.__configs[key] = {'key': key, 'values': val, 'row': self.__lines, 'separator': ' '}

        if isinstance(val, list):
            print("here 1")
            self.__configs[key]['values'].insert(0, key)
            self.__changed_lines[self.__configs[key]['row']] = self.__configs[key]['separator'] \
                .join(self.__configs[key]['values'])
        else:
            try:
                self.__changed_lines[self.__configs[key]['row']] = key + self.__configs[key]['separator'] + val

            except Exception as e:
                print(Exception)
                print(e)
        if (apply):
            self.apply_config()

    def print_output(self):
        for item in self.__configs.values():
            print(
                f"  {MyColors.HEADER}{item['key']}{item['separator']}{MyColors.OKGREEN}{item['values']}{MyColors.ENDC}")
        print("\n")

    @staticmethod
    def get_instance():
        if not SSH.__instance:
            try:
                SSH.__instance = SSH()
            except FileNotFoundError as exception:
                print(f"File Not Found {exception}")
                return None

        return SSH.__instance

    def apply_config(self):
        with open('/etc/ssh/sshd_config_temp', 'r') as file:
            original_file = file.readlines()
            for item in self.__changed_lines.items():
                original_file[item[0] - 1] = item[1] + "\n"
        with open('/etc/ssh/sshd_config_temp', 'w') as file:
            file.writelines(original_file)
