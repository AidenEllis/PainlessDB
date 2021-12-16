import os
import unittest
from datetime import datetime
from painlessdb import Schema, PainlessDB
from painlessdb.core.exceptions import UnexpectedDataType, ModelDoesntExist, FieldKeyDoesntExist


class TestDatabaseExceptions(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseExceptions, self).__init__(*args, **kwargs)
        self.db_path = os.path.join(os.getcwd(), 'test.pldb')
        self.schema_data = {
            'TestModels': {
                'field_1': Schema.types.text(),
                'field_2': Schema.types.int(),
                'field_3': Schema.types.bool(),
                'field_4': Schema.types.float(),
                'field_5': Schema.types.list(),
                'field_6': Schema.types.dict(),
                'field_7': Schema.types.datetime(),
                'field_8': Schema.types.text(),
            }
        }

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_exception_UnexpectedDataType(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        self.assertRaises(UnexpectedDataType, lambda: database.create('TestModels', fields=database.fields(field_1=1)))

    def test_exception_ModelDoesntExist(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        self.assertRaises(ModelDoesntExist, lambda: database.create('DummyIDK', fields=database.fields(field_1='OOF')))

    def test_exception_FieldKeyDoesntExist(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        self.assertRaises(FieldKeyDoesntExist, lambda: database.create('TestModels', fields=database.fields(fx='OOF')))
