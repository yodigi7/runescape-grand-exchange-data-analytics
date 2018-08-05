import unittest

import multiprocessing

from database_services.database import in_database


class TestInDatabase(unittest.TestCase):

    def test_get_days_for_item_fire_rune_has_many_days(self):
        self.assertTrue(len(in_database.get_days_for_item(554, multiprocessing.Lock())) > 100)

    def test_get_days_for_item_fake_item_has_no_days(self):
        self.assertTrue(len(in_database.get_days_for_item(100000, multiprocessing.Lock())) is 0)

    def test_new_days_returns_empty_list_given_all_days(self):
        lock = multiprocessing.Lock()
        self.assertEqual([],
                         in_database.determine_new_days(554, in_database.get_days_in_database(554, lock), lock))

if __name__ == '__main__':
    unittest.main()
