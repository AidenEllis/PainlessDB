import ast
import linecache
from core import Schema


class PainlessDB:
    """
    Painless Database Main Class.
    """

    def __init__(self, path_name: str, schema_data: dict):
        self.path = path_name
        self.schema = Schema.build(schema_data, silent=False)

    @staticmethod
    def get_data_from_db_file(file_path: str):
        """
        :param file_path: database.pldb file path.
        :return: database Data.
        """
        data_from_file = linecache.getline(file_path, 5)
        print(data_from_file)
        if data_from_file:
            data_dict_from_file = ast.literal_eval(data_from_file)

            return data_dict_from_file
        return {}


print(PainlessDB.get_data_from_db_file('../test.pldb'))

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
