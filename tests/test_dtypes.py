import os
import unittest
from datetime import datetime
from painlessdb import Schema, PainlessDB


class TestDatabaseDataTypes(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseDataTypes, self).__init__(*args, **kwargs)
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

    def test_type_returns(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        database.create('TestModels', fields=database.fields(
            field_1='This is a text',
            field_2=78,
            field_3=True,
            field_4=12.6812,
            field_5=['apple', 'berry', 'banana'],
            field_6={'a': 1, 'b': 2, 'c': 3},
            field_7=datetime.now(),
        ))

        data = database.get('TestModels', where=database.where(id=1), multiple=False)

        self.assertEqual(type(data.field_1), str)
        self.assertEqual(type(data.field_2), int)
        self.assertEqual(type(data.field_3), bool)
        self.assertEqual(type(data.field_4), float)
        self.assertEqual(type(data.field_5), list)
        self.assertEqual(type(data.field_6), dict)
        self.assertEqual(type(data.field_7), datetime)

    def test_field_defaults(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        database.create('TestModels', fields=database.fields(field_8='This is a dummy field 8 text'))
        data = database.get('TestModels', where=database.where(id=1), multiple=False)

        self.assertEqual(data.field_1, '')
        self.assertEqual(data.field_2, 0)
        self.assertEqual(data.field_3, False)
        self.assertEqual(data.field_4, 0.0)
        self.assertEqual(data.field_5, [])
        self.assertEqual(data.field_6, {})
        self.assertEqual(data.field_7, None)


if __name__ == '__main__':
    unittest.main()
