class UnexpectedDataType(Exception):
    def __init__(self, expected_type, got_type, field_key):
        self.expected_type = expected_type
        self.got_type = got_type
        self.field_key = field_key

    def __str__(self):
        return f"\nError: Got unexpected field('{self.field_key}') value type, expected '{self.expected_type}' " \
               f"but got '{self.got_type}'"


class FieldKeyDoesntExist(Exception):
    def __init__(self, group, field_key):
        self.group = group
        self.field_key = field_key

    def __str__(self):
        return f"\nField key '{self.field_key}' doesn't exist in database model's('{self.group}') schema."


class ModelDoesntExist(Exception):
    def __init__(self, model_name):
        self.model_name = model_name

    def __str__(self):
        return f"\nModel '{self.model_name}' doesn't exist in database schema."
