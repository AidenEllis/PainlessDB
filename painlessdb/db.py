import ast
from core import Schema
from utils import ObjectMapDict


class PainlessDB:
    """
    Painless Database Main Class.
    """

    def __init__(self, file_path_name: str, schema_data: dict):
        self.file_path = file_path_name
        self.schema = Schema.build(schema_data)
        self.temp_data = []
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

    def get(self, model_name: str, where=None, multiple: bool = True):
        data = self.get_data_from_db_file(self.file_path)
        data_result = None
        schema_data = self.schema
        model_type_group = "GROUP"
        model_type_static = "STATIC"

        model_type = None

        for group_model in schema_data['groups']:
            if group_model['name'] == model_name:
                model_type = model_type_group

        if not model_type:
            for static_model in schema_data['statics']:
                if static_model['name'] == model_name:
                    model_type = model_type_static

        if not model_type:
            quit(f"Model '{model_name}' doesn't exit.")

        if model_type:
            data_result = data[model_name]

            if model_type == model_type_group:
                data_result = [ObjectMapDict(**data) for data in data_result]
        data_result_multiple = []
        if where:
            if model_type == model_type_static:
                exit(f"[PainlessDB]: Can't use 'where()', You can't search 'Static' data type.")

            if type(data_result) is list:
                # where_data = None

                for content in data_result:
                    found_where = False
                    for key, val in where.items():
                        try:
                            if content[key] == val:
                                if multiple:
                                    data_result_multiple.append(content)
                                found_where = True
                            else:
                                found_where = False
                        except KeyError:
                            raise KeyError(f"[PainlessDB]: Error while processing PainlessDB.where({where}), "
                                           f"Field '{key}' doesn't exist in Database schema.")
                    if found_where and not multiple:
                        data_result = content
                        break

        if multiple:
            return data_result_multiple
        return data_result

    @staticmethod
    def where(**kwargs):
        return kwargs


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
#
# import random
#
database = PainlessDB('../test.pldb', schema)
a = database.get('users', where=database.where(username="Bot-User-28"))
print(a[1].username)

#
# for i in range(1):
#     database.create('users', username=str(f'Bot-User-{i}'), password=str(random.randint(10000, 99999)))
#     print(f"Successfully Created Bot-User-{i}.")
