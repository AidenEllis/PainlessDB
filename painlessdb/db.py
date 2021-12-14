import ast
import linecache
from core import Schema


class PainlessDB:
    """
    Painless Database Main Class.
    """

    def __init__(self, file_path_name: str, schema_data: dict):
        self.file_path = file_path_name
        self.schema = Schema.build(schema_data)
        Schema.write(file_path=self.file_path, raw_schema_data=schema_data)

    @staticmethod
    def get_data_from_db_file(file_path: str):
        """
        :param file_path: database.pldb file path.
        :return: database Data.
        """

        with open(file_path, 'r') as file:
            lines = file.readlines()
            lineno = 5
            data_from_file = ''

            if 1 <= lineno <= len(lines):
                data_from_file = lines[lineno - 1]

        if data_from_file:
            data_dict_from_file = ast.literal_eval(data_from_file)

            return data_dict_from_file
        return {}

    def create(self, group: str, **kwargs):
        user_kwarg_dict = kwargs

        db_data = self.get_data_from_db_file(self.file_path)
        db_data[group].append(user_kwarg_dict)
        Schema.WriteData(data=db_data, file_path=self.file_path)


schema = {
    'users': {
        'username': Schema.types.text(),
        'password': Schema.types.text()
    },

    'dontations': {
        'user': Schema.types.text(),
        'amount': Schema.types.int()
    },

    'earnings': Schema.types.int(),
    'Subscribers': Schema.types.int()
}

# print(json.dumps(Schema.build(schema), sort_keys=True, indent=2))

# import random
#
# database = PainlessDB('../test.pldb', schema)
#
#
# for i in range(20):
#     database.create('users', username=str(f'Bot-User-{i}'), password=str(random.randint(10000, 99999)))
#     print(f"Successfully Created Bot-User-{i}.")
