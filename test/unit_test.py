import unittest

class TestApp(unittest.TestCase):
    
    def test_yes(self):
        self.assertEqual("yes","yes")

    def test_one_plus_one(self):
        self.assertEqual(1+1,2)

    def test_dustin_fav_food(self):
        dustin_fav_food = "tomato"
        self.assertEqual(dustin_fav_food,"tomato")    

    def test_tristan_fav_food(self):
        tristan_fav_food = "beets"
        self.assertEqual(tristan_fav_food,"beets")

    def test_sean_fav_food(self):
        sean_fav_food = "curry beef"
        self.assertEqual(sean_fav_food,"curry beef")    

if __name__ == '__main__':
    unittest.main()
