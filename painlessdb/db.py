import ast
import ujson
from ast import literal_eval
from datetime import datetime
from .core.exceptions import *
from distutils.util import strtobool
from .core import Schema, DataObject
from .utils.converter import datetimeToStr, singleQuoteToDoubleQuote


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
            fixed_data = singleQuoteToDoubleQuote(
                data_from_file.replace("True", "true").replace("None", "null").replace("False", "false"))
            data_dict_from_file = ujson.loads(fixed_data)
            return data_dict_from_file
        return {}

    def increaceId(self, group: str):
        with open(self.file_path, 'r', encoding='utf-8') as file_:
            db_data = file_.readlines()
            track_dict_current = ast.literal_eval(db_data[7])

            track_dict_current[f"{group}_id_track"] = int(track_dict_current[f"{group}_id_track"]) + 1
            db_data[7] = str(track_dict_current) + "\n"
            file_.flush()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.writelines(db_data)
            file.flush()

    def validate_fields(self, model_name: str, fields: dict, model_type=None, update=False):
        fields_schema = None
        all_fields = []
        static_field_name = None

        if model_type == "GROUP":
            for ind, grp in enumerate(self.schema['groups']):
                if grp['name'] == model_name:
                    fields_schema = self.schema['groups'][ind]['schema']

        elif model_type == "STATIC":
            for ind, stat in enumerate(self.schema['statics']):
                if stat['name'] == model_name:
                    static_field_name = self.schema['statics'][ind]['name']
                    fields_schema = {static_field_name: self.schema['statics'][ind]['datatype']}
                    fields = {self.schema['statics'][ind]['name']: fields['value']}

        if not fields_schema:
            raise ModelDoesntExist(model_name=model_name)

        if model_type == "GROUP" and not update:
            for f in fields_schema:
                all_fields.append(f)

            x = [a for a in fields]

            default_fields = list(set(all_fields) ^ set(x))

            for fkey in fields.keys():
                if fkey not in list(fields_schema.keys()) and fkey != 'id':
                    raise FieldKeyDoesntExist(field_key=fkey, group=model_name)

            for df in default_fields:
                if df == 'id':
                    continue
                dtype, dfval = str(fields_schema[df]).split('|')

                if dtype == 'text':
                    fields[df] = str(dfval)

                elif dtype == 'int':
                    fields[df] = int(dfval)

                elif dtype == 'float':
                    fields[df] = float(dfval)

                elif dtype == 'dict':
                    fields[df] = dict(literal_eval(dfval))

                elif dtype == 'list':
                    fields[df] = list(literal_eval(dfval))

                elif dtype == 'boolean':
                    fields[df] = bool(strtobool(dfval))

                elif dtype == 'datetime':
                    fields[df] = None

        for fkey, fval in fields.items():
            if fkey in list(fields_schema.keys()) or fkey == 'id':
                if fkey == "id":
                    continue
                dtype, dfval = str(fields_schema[fkey]).split('|')

                if dtype == 'text':
                    if type(fields[fkey]) is str:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='str', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == 'int':
                    if type(fields[fkey]) is int:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='int', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == 'float':
                    if type(fields[fkey]) is float:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='float', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == 'boolean':
                    if type(fields[fkey]) is bool:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='bool', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == 'list':
                    if type(fields[fkey]) is list:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='list', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == 'dict':
                    if type(fields[fkey]) is dict:
                        pass
                    else:
                        raise UnexpectedDataType(expected_type='dict', got_type=type(fields[fkey]), field_key=fkey)

                elif dtype == "datetime":
                    if type(fields[fkey]) is datetime or type(fields[fkey]) is None:
                        if type(fields[fkey]) is datetime:
                            dt_str_value = datetimeToStr(fields[fkey])
                            fields[fkey] = dt_str_value
                    else:
                        if (fields[fkey]) is not None:
                            raise UnexpectedDataType(expected_type='datetime.datetime', got_type=type(fields[fkey]),
                                                     field_key=fkey)

            else:
                raise FieldKeyDoesntExist(field_key=fkey, group=model_name)

        if model_type == "STATIC":
            return fields[static_field_name]

        return fields

    def create(self, group: str, fields):
        user_kwarg_dict = self.validate_fields(group, fields, model_type="GROUP")
        user_kwarg_dict['id'] = self.get_id(group)
        db_data = self.get_data_from_db_file(self.file_path)
        db_data[group].append(user_kwarg_dict)
        Schema.WriteData(data=db_data, file_path=self.file_path)
        self.increaceId(group)

    def get(self, model_name: str, where=None, multiple: bool = True, advanced=False, bypass_static_dt_error=False):
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

        if bypass_static_dt_error and model_type == "STATIC":
            where = None

        if not model_type:
            raise ModelDoesntExist(model_name=model_name)

        if model_type:
            data_result = data[model_name]
            metadata = {'model_type': model_type, 'model_name': model_name}

            if model_type == model_type_group:
                data_result = [DataObject(data=data, model_name=model_name, database=self, metadata=metadata) for data
                               in data_result]

            elif model_type == model_type_static:
                d_ = {'value': data_result}
                data_result = DataObject(data=d_, model_name=model_name, database=self, metadata=metadata)

        if model_type == model_type_group:
            i = None
            data_changes = []
            field_schema = schema_data['groups']

            for ind, f in enumerate(field_schema):
                if f['name'] == model_name:
                    i = ind
                    break

            field_schema = schema_data['groups'][i]['schema']
            for fk, fv in field_schema.items():
                ftype = str(fv).split("|")[0]
                if ftype == 'datetime':
                    data_changes.append((fk, ftype))

            if model_type == model_type_group:
                for ind, data_ in enumerate(data_result):
                    for f, t in data_changes:
                        if f in data_.data:
                            if t == 'datetime':
                                dt_data_str = data_result[i].data[f]

                                if dt_data_str:
                                    dt_values = str(dt_data_str).split('|')[0:-1]
                                    dt_obj = datetime(*map(int, dt_values))
                                    data_result[i - ind - 1].data[f] = dt_obj

        if model_type == "STATIC":
            i_ = None
            for ind, s in enumerate(schema_data['statics']):
                if s['name'] == model_name:
                    i_ = ind
                    break

            if schema_data['statics'][i_]['datatype'].split('|')[0] == "datetime":
                if data_result.value is not None:
                    dt_values = str(data_result.value).split('|')[0:-1]
                    dt_obj = datetime(*map(int, dt_values))
                    data_result.value = dt_obj

        if not where:
            advanced_data = {}
            if advanced:
                advanced_data['model_type'] = model_type
                advanced_data['data_result'] = data_result
                if model_type == model_type_static:
                    advanced_data['data_result'] = data_result

                return advanced_data
            if not multiple and len(data_result) > 1:
                return data_result[0]

            return data_result

        data_result_multiple = []
        found_where = False

        if where:
            if model_type == model_type_static:
                raise Exception(f"[PainlessDB]: Can't use 'where()' for 'Static' data type.")

            if type(data_result) is list:
                for content in data_result:
                    content_match = []
                    for key, where_val in where.items():
                        try:
                            if content.data[key] == where_val:
                                content_match.append(True)

                        except KeyError:
                            raise KeyError(f"[PainlessDB]: Error while processing PainlessDB.where({where}), "
                                           f"Field '{key}' doesn't exist in Database schema.")

                    if len(content_match) == len(where):
                        found_where = True

                    if found_where and model_type == model_type_group:
                        data_result_multiple.append(content)

                    if found_where and not multiple:
                        data_result = content
                        break

                    found_where = False

        advanced_data = {}

        if advanced:
            advanced_data['model_type'] = model_type
            advanced_data['data_result'] = data_result
            if model_type == model_type_static:
                advanced_data['data_result'] = data_result
            if not multiple and not found_where and model_type != model_type_static:
                advanced_data['data_result'] = None
            if multiple and model_type != model_type_static:
                advanced_data['data_result'] = data_result_multiple

            return advanced_data

        if model_type == model_type_static:
            return data_result

        if not multiple and not found_where:
            return None

        if multiple:
            return data_result_multiple

        return data_result

    def update(self, model_name: str, fields=None, where=None, search_fail_silently=False, value=None,
               bypass_static_dt_error=False):
        content_data = self.get(model_name, where=where, advanced=True, multiple=False,
                                bypass_static_dt_error=bypass_static_dt_error)

        if content_data['model_type'] == "GROUP":
            fields = self.validate_fields(model_name, fields, model_type=content_data['model_type'], update=True)

        elif content_data['model_type'] == "STATIC":
            value = self.validate_fields(model_name, {'value': value}, model_type=content_data['model_type'],
                                         update=True)

        if bypass_static_dt_error and content_data['model_type'] == "STATIC":
            if value is None and fields:
                value = fields['value']
                fields = None
                where = None

        model_type = content_data['model_type']
        data_result = content_data['data_result'].data
        data_result_ = dict(content_data['data_result'].data)

        if not fields and not value:
            raise Exception(f"[PainlessDB]: Content update Failed. Please provide fields in update(where=?)")

        if model_name and fields and content_data['model_type'] == "GROUP":
            pass

        if data_result is None or data_result == []:
            if not search_fail_silently:
                raise Exception(f"[PainlessDB]: Content update Failed."
                                f"Couldn't find the content specified with where({where}).")

        if model_type == "GROUP":
            for field_data in data_result.items():
                if field_data[0] in fields.keys():
                    data_result[field_data[0]] = fields[field_data[0]]

        if model_type == "GROUP":
            for fkey, fval in fields.items():
                if type(fval) == datetime:
                    dt_str_value = datetimeToStr(fval)
                    fields[fkey] = dt_str_value

            for fk, fv in data_result.items():
                if type(fv) == datetime:
                    dt_str_value = datetimeToStr(fv)
                    data_result[fk] = dt_str_value
                    data_result_[fk] = dt_str_value

            data_from_db = self.get_data_from_db_file(self.file_path)
            ind = None

            for ind_, data in enumerate(data_from_db[model_name]):
                if data['id'] == data_result_['id']:
                    ind = ind_
                    break

            data_from_db[model_name][ind] = data_result
            Schema.WriteData(data_from_db, file_path=self.file_path)

        elif model_type == "STATIC":
            if type(value) == datetime:
                dt_str_value = datetimeToStr(value)
                value = dt_str_value

            data_from_db = self.get_data_from_db_file(self.file_path)
            data_from_db[model_name] = value
            Schema.WriteData(data_from_db, file_path=self.file_path)

    def delete(self, group_name: str, where=None, metadata=None):
        model_type = None
        content_id = None

        if where and not metadata:
            content_data = self.get(group_name, where=where, advanced=True, multiple=False)
            model_type = content_data['model_type']
            content_id = dict(content_data['data_result'].data)['id']

        elif metadata and not where:
            model_type = metadata['model_type']
            content_id = metadata['id']

        if model_type == "GROUP":
            data_from_db = self.get_data_from_db_file(self.file_path)
            for ind, content in enumerate(data_from_db[group_name]):
                if content['id'] == content_id:
                    del data_from_db[group_name][ind]
                    break

            Schema.WriteData(data_from_db, file_path=self.file_path)

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

    @staticmethod
    def fields(**kwargs):
        return kwargs

    @staticmethod
    def where(**kwargs):
        return kwargs
