import os
import unittest
from painlessdb import Schema


class TestDatabaseSchema(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseSchema, self).__init__(*args, **kwargs)
        self.db_path = os.path.join(os.getcwd(), 'test.pldb')
        self.schema_data = {
            'users': {
                'username': Schema.types.text(),
                'password': Schema.types.text(),
                'is_active': Schema.types.bool()
            },

            'donations': {
                'username': Schema.types.text(),
                'amount': Schema.types.int()
            },

            'UserCount': Schema.types.int()
        }

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_schema_build(self):
        expected_schema = {
            'groups': [
                {
                    'name': 'users',
                    'schema': {
                        'username': 'text|',
                        'password': 'text|',
                        'is_active': 'boolean|False'
                    }
                },
                {
                    'name': 'donations',
                    'schema': {
                        'username': 'text|',
                        'amount': 'int|0',
                    }
                }
            ],
            'statics': [
                {
                    'name': 'UserCount',
                    'datatype': 'int|0'
                }
            ]
        }
        schema = Schema.build(self.schema_data)
        self.assertEqual(expected_schema, schema)

    def test_schema_write_data(self):
        expected_result = {
            "raw_schema_data": {
                "users": {
                    "username": "text|",
                    "password": "text|",
                    "is_active": "boolean|False",
                },
                "donations": {"username": "text|", "amount": "int|0"},
                "UserCount": "int|0",
            },
            "schema_data_dict": {"users": [], "donations": [], "UserCount": 0},
            "track_data_dict": {"users_id_track": 0, "donations_id_track": 0},
        }

        schema_write_data = Schema.write(file_path=self.db_path, raw_schema_data=self.schema_data, testing=True)
        self.assertEqual(expected_result, schema_write_data)


if __name__ == '__main__':
    unittest.main()
