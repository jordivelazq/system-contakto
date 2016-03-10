# """
# This file demonstrates writing tests using the unittest module. These will pass
# when you run "manage.py test".

# Replace this with more appropriate tests for your application.
# """

# from django.test import TestCase


# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

import unittest
import datetime

from .services import InvestigacionService

class TestStringMethods(unittest.TestCase):

  def test_trans_date(self):
		d = datetime.datetime.today()
		date = InvestigacionService.trans_date(d)
		self.assertEqual(len(date), 11)

if __name__ == '__main__':
    unittest.main()