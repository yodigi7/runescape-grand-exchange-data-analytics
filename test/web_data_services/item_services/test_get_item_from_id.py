import unittest
from web_data_services.item_services.get_item_from_id import get_item_from_id


class TestGetItemFromId(unittest.TestCase):

    def test_554_is_fire_rune(self):
        item = get_item_from_id(554)
        self.assertEqual(554, item.item_id)
        self.assertEqual('Fire rune', item.name)


if __name__ == '__main__':
    unittest.main()
