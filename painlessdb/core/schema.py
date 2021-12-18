import os
import ast
import linecache
from distutils.util import strtobool
from painlessdb.utils import ObjectMapDict


class SchemaTypes:
    def __init__(self):
        self.int = self.typeInt
        self.text = self.typeText
        self.bool = self.typeBool
        self.float = self.typeFloat
        self.list = self.typeList
        self.dict = self.typeDict
        self.datetime = self.typeDatetime

    @staticmethod
    def typeInt(default=0):
        return f"int|{default}"

    @staticmethod
    def typeBool(default=False):
        return f"boolean|{default}"

    @staticmethod
    def typeText(default=''):
        return f"text|{default}"

    @staticmethod
    def typeDatetime(default=None):
        return f"datetime|{default}"

    @staticmethod
    def typeFloat(default=0.0):
        return f"float|{default}"

    @staticmethod
    def typeList(default=None):
        if not default:
            default = []

        return f"list|{default}"

    @staticmethod
    def typeDict(default=None):
        if not default:
            default = {}

        return f"dict|{default}"


class Schema:
    types = SchemaTypes()
    SCHEMA_SPECIAL_KW = "------------------------------SCHEMA------------------------------"
    DATA_SPECIAL_KW = "------------------------------DATA------------------------------"
    TRACK_SPECIAL_KW = "------------------------------TRACK------------------------------"

    def __init__(self):
        self.dataTypeList = ["text", "int", "datetime", "boolean", "blob", "float"]

    @staticmethod
    def build(raw_schema_data: dict, silent=True):
        if not silent:
            print("[PainlessDB]: Building schema using schema data.")

        schema_data = ObjectMapDict()
        schema_data.groups = []
        schema_data.statics = []

        raw_schema_data_items = list(raw_schema_data.items())

        for item in raw_schema_data_items:
            if type(item[1]) is dict:
                schema_data.groups.append({"name": item[0], "schema": item[1]})
            else:
                schema_data.statics.append({"name": item[0], "datatype": item[1]})

        return schema_data

    @staticmethod
    def get_default(schema_val):
        dtype, dfval = str(schema_val).split('|')

        if dtype == 'text':
            return str(dfval)

        elif dtype == 'int':
            return int(dfval)

        elif dtype == 'float':
            return float(dfval)

        elif dtype == 'dict':
            return dict(ast.literal_eval(dfval))

        elif dtype == 'list':
            return list(ast.literal_eval(dfval))

        elif dtype == 'boolean':
            return bool(strtobool(dfval))

        elif dtype == 'datetime':
            return None

        else:
            return None

    @staticmethod
    def write(file_path: str, raw_schema_data: dict, testing=False):
        if str(file_path)[-5:] != '.pldb':
            quit("[PainlessDB]: Database extention must be .pldb (eg. database.pldb)")

        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass

        with open(file_path, 'r+') as db_file:
            with open(file_path, 'r') as f:
                get_all = f.readlines()

            if get_all:
                schema_data_from_file = linecache.getline(file_path, 2)
                schema_data_dict_from_file = ast.literal_eval(schema_data_from_file)

                if schema_data_dict_from_file != raw_schema_data:
                    print(f"[PainlessDB]: Different Database Raw Schema Detected"
                          f"\nAre you sure you want to change the Schema in the Database? > '{file_path}'")
                    confirm_input = input("Type 'Yes' or 'No': ")
                    while confirm_input.lower() not in ["yes", "no"]:
                        confirm_input = input("Type 'Yes' or 'No':")

                    if confirm_input == 'yes':
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = file.readlines()
                            data[0] = Schema.SCHEMA_SPECIAL_KW + '\n'
                            data[1] = str(raw_schema_data) + '\n'
                            data[2] = Schema.SCHEMA_SPECIAL_KW + '\n'

                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(data)

                        print("[PainlessDb]: Database Schema Has Been Changed Successfully.")
                    else:
                        quit("[PainlessDB]: Canceled Schema Change.")

            else:
                schema_data = Schema.build(raw_schema_data)
                schema_data_dict = {}

                for group in schema_data.groups:
                    schema_data_dict[group['name']] = []

                for static in schema_data.statics:
                    schema_data_dict[static['name']] = Schema.get_default(static['datatype'])

                track_data_dict = {}
                for group in schema_data.groups:
                    track_data_dict[f"{group['name']}_id_track"] = 0

                if testing:
                    test_data = {
                        'raw_schema_data': raw_schema_data,
                        'schema_data_dict': schema_data_dict,
                        'track_data_dict': track_data_dict
                    }
                    return test_data

                db_file.writelines(f"{Schema.SCHEMA_SPECIAL_KW}\n{raw_schema_data}\n{Schema.SCHEMA_SPECIAL_KW}\n"
                                   f"{Schema.DATA_SPECIAL_KW}\n{schema_data_dict}\n{Schema.DATA_SPECIAL_KW}\n"
                                   f"{Schema.TRACK_SPECIAL_KW}\n{track_data_dict}\n{Schema.TRACK_SPECIAL_KW}\n")

    @staticmethod
    def WriteData(data: dict, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file_:
            db_data = file_.readlines()
            db_data[4] = str(data) + '\n'
            file_.flush()
            file_.close()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(db_data)
            file.flush()
            file.close()
