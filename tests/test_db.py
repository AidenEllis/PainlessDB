import os
import unittest
from painlessdb import Schema, PainlessDB


class TestDatabase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabase, self).__init__(*args, **kwargs)
        self.db_path = os.path.join(os.getcwd(), 'test.pldb')
        self.schema_data = {
            'users': {
                'username': Schema.types.text(),
                'password': Schema.types.text(),
            },

            'donations': {
                'username': Schema.types.text(),
                'amount': Schema.types.int()
            },

            'usercount': Schema.types.int(default=1)
        }

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_create_and_get(self):
        database = PainlessDB(file_path_name=self.db_path,  schema_data=self.schema_data)

        database.create('users', fields=database.fields(username='Gumball Watterson', password='deeznuts69'))
        data_1 = database.get('users', where=database.where(username='Gumball Watterson'), multiple=False)
        self.assertEqual(data_1.data, {'username': 'Gumball Watterson', 'password': 'deeznuts69', 'id': 1})

        data_2 = database.get('users', where=database.where(username='Gumball Watterson', password='deeznuts69'),
                              multiple=False)
        self.assertEqual(data_2.data, {'username': 'Gumball Watterson', 'password': 'deeznuts69', 'id': 1})

        for i in range(1, 9 + 1):
            database.create('users', fields=database.fields(username=f'Bot-User-{i}', password=f'sungondeeznuts-{i}'))
            print(f"[UnitTest]: Created Bot-User-{i}")

        data_3 = database.get('users')
        self.assertEqual(len(data_3), 10)

    def test_database_delete(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        for i in range(1, 10 + 1):
            database.create('users', fields=database.fields(username=f'Bot-User-{i}', password=f'sungondeeznuts-{i}'))
            print(f"[UnitTest]: Created Bot-User-{i}")

        database.delete('users', where=database.where(username="Bot-User-1"))
        data_1 = database.get('users', where=database.where(username="Bot-User-1"), multiple=False)
        self.assertIsNone(data_1)

        data_2 = database.get('users')
        for i, content in enumerate(data_2):
            content.delete()
            print(f"[UnitTest]: Deleted Bot-User-{i}")
        self.assertEqual(len(database.get('users')), 0)

    def test_database_update(self):
        database = PainlessDB(file_path_name=self.db_path, schema_data=self.schema_data)

        database.create('users', fields=database.fields(username='Gumball Watterson', password='deeznuts69'))

        data_1 = database.get('users', where=database.where(username='Gumball Watterson'), multiple=False)
        data_1.password = 'newpassword69'
        data_1.update()
        data_2 = database.get('users', where=database.where(username='Gumball Watterson'), multiple=False)
        self.assertEqual(data_2.password, 'newpassword69')

        data_2 = database.get('users', where=database.where(username='Gumball Watterson'), multiple=False)
        data_2.username = 'Gumball Deeznuts'
        data_2.password = 'newgumpass0'
        data_2.update()
        data_3 = database.get('users', where=database.where(username='Gumball Deeznuts', password='newgumpass0'),
                              multiple=False)
        self.assertIsNotNone(data_3)

        database.update('users', where=database.where(username='Gumball Deeznuts', password='newgumpass0'),
                        fields=database.fields(username='Gumball'))
        data_4 = database.get('users', where=database.where(username='Gumball'), multiple=False)
        self.assertEqual(data_4.username, 'Gumball')
        print("Debug 3: ", database.get('users', where=database.where(username='Gumball', password='newgumpass0')))
        database.update('users', where=database.where(username='Gumball', password='newgumpass0'),
                        fields=database.fields(username='Gumball Watterson', password='herewegoagain18'))
        data_5 = database.get('users', where=database.where(username='Gumball Watterson'), multiple=False)
        self.assertEqual(data_5.username, 'Gumball Watterson')
        self.assertEqual(data_5.password, 'herewegoagain18')

        database.update('usercount', value=652)
        data_6 = database.get('usercount')
        self.assertEqual(data_6.value, 652)


if __name__ == '__main__':
    unittest.main()
