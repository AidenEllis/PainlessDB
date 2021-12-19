import copy


class DataObject:
    debug = False

    def __init__(self, data: dict, model_name: str, database, metadata: dict = None):
        self.data = data
        self.model_name = model_name
        self.database = database
        self.__metadata__ = metadata

    def update(self, fields=None, search_fail_silently=False, value=None):
        if not fields and not value:
            new_data = copy.deepcopy(self.data)
            for fkey, fval in new_data.items():
                new_data[fkey] = getattr(self, fkey)

            obj_id = self.Metadata['id']
            self.database.update(model_name=self.model_name, fields=new_data, where={'id': obj_id},
                                 search_fail_silently=search_fail_silently, value=value, bypass_static_dt_error=True)

        else:
            if value and not fields:
                self.database.update(model_name=self.model_name, search_fail_silently=search_fail_silently,
                                     value=value)
            else:
                self.database.update(model_name=self.model_name, fields=fields, where=self.data,
                                     search_fail_silently=search_fail_silently, value=value)

    def delete(self):
        self.database.delete(group_name=self.model_name, metadata=self.Metadata)

    def __getattr__(self, attr):
        return self.data[attr]

    def __str__(self):
        if not self.debug:
            return f"DataObject({self.model_name})"
        else:
            return f"Obj: {str(self.data)}"

    @property
    def Metadata(self):
        if self.data.get('id', None):
            self.__metadata__['id'] = self.data['id']

        return self.__metadata__
