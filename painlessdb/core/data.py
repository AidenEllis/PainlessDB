class DataObject:
    debug = True

    def __init__(self, data: dict, model_name: str, database):
        self.data = data
        self.model_name = model_name
        self.database = database
        self.value = None

    def delete(self):
        self.database.delete(group_name=self.model_name, where=self.data)

    def update(self, fields=None, search_fail_silently=False, value=None):
        if not fields and not value:
            new_data = dict(self.data)
            for fkey, fval in new_data.items():
                new_data[fkey] = getattr(self, fkey)

            self.database.update(model_name=self.model_name, fields=new_data, where=self.data,
                                 search_fail_silently=search_fail_silently, value=value, bypass_static_dt_error=True)

        else:
            if value and not fields:
                self.database.update(model_name=self.model_name, search_fail_silently=search_fail_silently, value=value)
            else:
                self.database.update(model_name=self.model_name, fields=fields, where=self.data,
                                     search_fail_silently=search_fail_silently, value=value)

    def __getattr__(self, attr):
        return self.data[attr]

    def __str__(self):
        if not self.debug:
            return f"DataObject({str(list(self.data.keys()))[1:-1]})"
        else:
            return f"Obj: {str(self.data)}"
