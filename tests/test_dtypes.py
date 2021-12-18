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
            },

            'static_1': Schema.types.text(),
            'static_2': Schema.types.int(),
            'static_3': Schema.types.bool(),
            'static_4': Schema.types.float(),
            'static_5': Schema.types.list(),
            'static_6': Schema.types.dict(),
            'static_7': Schema.types.datetime()
        }

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_type_returns(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        dt_obj = datetime.now()
        database.create('TestModels', fields=database.fields(
            field_1='This is a text',
            field_2=78,
            field_3=True,
            field_4=12.6812,
            field_5=['apple', 'berry', 'banana'],
            field_6={'a': 1, 'b': [1, 2, '3'], 'c': True},
            field_7=dt_obj,
        ))

        data = database.get('TestModels', where=database.where(id=1), multiple=False)

        self.assertEqual(data.field_1, 'This is a text')
        self.assertEqual(data.field_2, 78)
        self.assertEqual(data.field_3, True)
        self.assertEqual(data.field_4, 12.6812)
        self.assertEqual(data.field_5, ['apple', 'berry', 'banana'])
        self.assertEqual(data.field_6, {'a': 1, 'b': [1, 2, '3'], 'c': True})
        self.assertEqual(data.field_7, dt_obj)

        dt_obj = datetime.now()
        database.update('static_1', value='just a text')
        database.update('static_2', value=120)
        database.update('static_3', value=True)
        database.update('static_4', value=3.8129)
        database.update('static_5', value=['120B', '129D', 12, False, {'as': [1, 2, 'b']}])
        database.update('static_6', value={'a1': 1, 'a2': False, 'l': ['b', {'a': [1, 2, 3]}]})
        database.update('static_7', value=dt_obj)

        self.assertEqual(database.get('static_1').value, 'just a text')
        self.assertEqual(database.get('static_2').value, 120)
        self.assertEqual(database.get('static_3').value, True)
        self.assertEqual(database.get('static_4').value, 3.8129)
        self.assertEqual(database.get('static_5').value, ['120B', '129D', 12, False, {'as': [1, 2, 'b']}])
        self.assertEqual(database.get('static_6').value, {'a1': 1, 'a2': False, 'l': ['b', {'a': [1, 2, 3]}]})
        self.assertEqual(database.get('static_7').value, dt_obj)

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

        self.assertEqual(database.get('static_1').value, '')
        self.assertEqual(database.get('static_2').value, 0)
        self.assertEqual(database.get('static_3').value, False)
        self.assertEqual(database.get('static_4').value, 0.0)
        self.assertEqual(database.get('static_5').value, [])
        self.assertEqual(database.get('static_6').value, {})
        self.assertEqual(database.get('static_7').value, None)


if __name__ == '__main__':
    unittest.main()
