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

    def create(self, group: str, fields):
        user_kwarg_dict = fields
        user_kwarg_dict['id'] = self.get_id(group)

        db_data = self.get_data_from_db_file(self.file_path)
        db_data[group].append(user_kwarg_dict)
        Schema.WriteData(data=db_data, file_path=self.file_path)
        self.increaceId(group)

    def increaceId(self, group: str):
        with open(self.file_path, 'r', encoding='utf-8') as file_:
            db_data = file_.readlines()
            track_dict_current = ast.literal_eval(db_data[7])
            print(track_dict_current)
            track_dict_current[f"{group}_id_track"] = int(track_dict_current[f"{group}_id_track"]) + 1
            db_data[7] = str(track_dict_current) + "\n"
            file_.flush()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.writelines(db_data)
            file.flush()

    def get(self, model_name: str, where=None, multiple: bool = True, advanced=False):
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
        found_where = False
        if where:
            if model_type == model_type_static:
                exit(f"[PainlessDB]: Can't use 'where()', You can't search 'Static' data type.")

            if type(data_result) is list:
                # where_data = None

                for content in data_result:
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

        adv_data = {}
        # print(data_result)
        if advanced:
            adv_data['model_type'] = model_type
            adv_data['data_result'] = data_result
            if model_type == model_type_static:
                adv_data['data_result'] = data_result
            if not multiple and not found_where and model_type != model_type_static:
                adv_data['data_result'] = None
            if multiple and model_type != model_type_static:
                adv_data['data_result'] = data_result_multiple

            return adv_data

        if model_type == model_type_static:
            return data_result

        if not multiple and not found_where:
            return None

        if multiple:
            return data_result_multiple

        return data_result

    def update(self, model_name: str, fields=None, where=None, search_fail_silently=False, value=None):
        content_data = self.get(model_name, where=where, advanced=True, multiple=False)
        model_type = content_data['model_type']
        data_result = content_data['data_result']
        data_result_ = content_data['data_result']

        if not fields and not value:
            exit(f"[PainlessDB]: Content update Failed. Please provide fields in update(where=?)")

        if data_result is None or data_result == []:
            if not search_fail_silently:
                exit(f"[PainlessDB]: Content update Failed."
                     f"Couldn't find the content specified with where({where}).")

        if model_type == "GROUP":
            for field_data in data_result.items():
                if field_data[0] in fields.keys():
                    data_result[field_data[0]] = fields[field_data[0]]

        if model_type == "GROUP":
            data_from_db = self.get_data_from_db_file(self.file_path)
            data_from_db[model_name][int(data_result_['id']) - 1] = data_result
            Schema.WriteData(data_from_db, file_path=self.file_path)

        elif model_type == "STATIC":
            data_from_db = self.get_data_from_db_file(self.file_path)
            data_from_db[model_name] = value
            Schema.WriteData(data_from_db, file_path=self.file_path)

    @staticmethod
    def fields(**kwargs):
        return kwargs

    @staticmethod
    def where(**kwargs):
        return kwargs

    def get_id(self, group_name: str):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            lineno = 8
            data_from_file = ''

            if 1 <= lineno <= len(lines):
                data_from_file = lines[lineno - 1]

        if data_from_file:
            data_dict_from_file = ast.literal_eval(data_from_file)

            id_ = int(data_dict_from_file[f"{group_name}_id_track"]) + 1
            return id_


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
# database.create('users', fields=database.fields(username='Gumball', password="hfa!@#h236(*79afsd_+0=dsafyb-8f"))
database.update('earnings', value=102)
# a = database.get('earnings', multiple=True)
# print(a)
# for i in range(1, 100):
#     a = database.get('users', where=database.where(username=f"Bot-User-{i}"))
#     print(a)

# import random
# for i in range(1, 101):
#     database.create('users', username=str(f'Bot-User-{i}'), password=str(random.randint(10000, 99999)))
#     print(f"Successfully Created Bot-User-{i}.")
