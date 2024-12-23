import unittest

from app import Superhero

class TestSuperhero(unittest.TestCase):
    def test_stringify(self):
        superhero = Superhero(name="Superman", strength_level=50)
        self.assertEqual(str(superhero),"Superman")

    def test_is_stronger_than_other_superhero(self):
        superhero = Superhero(name="Superman", strength_level=50)
        other_superhero = Superhero(name="Batman", strength_level=35)

        self.assertTrue(superhero.is_stronger_than(other_superhero))
        self.assertFalse(other_superhero.is_stronger_than(superhero))