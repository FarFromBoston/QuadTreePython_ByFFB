"""
READ ME:

!!! NOTE !!!
NB.1) Before proceeding to point (1) below,
      please make sure you have read the 'READ ME'
      section within the algorithm file 'Quadtrees_vs_Linear_Search1'.

NB.2) Please make sure package 'unittest' is installed in your current
      Python version running. Note this should be installed already with python
      upon python's download (PY versions 3.6+)



1) Please go to the line indicated with '#############' at the very bottom of
   this file

2) Comment out either line beneath it to run that program, Either the Tester
   or the actual algorithm

   
"""

import Quadtrees_vs_Linear_Search1 as QLS
import unittest


# All tests
# assert method types found at:
# https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
class TestMain(unittest.TestCase):

    def setUp(self):
        self.a_point = QLS.Point(1, (101,200))
        self.a_point2 = QLS.Point(2, (0,50))
        self.a_rectangle = QLS.Rectangle(100,100,300,300)
        self.a_rectangle2 = QLS.Rectangle(100,100,101,101)

        self.a_rectangle3 = QLS.Rectangle(0,100,99,300)
        self.a_rectangle4 = QLS.Rectangle(400,100,500,300)
        self.a_rectangle5 = QLS.Rectangle(100,0,300,99)
        self.a_rectangle6 = QLS.Rectangle(100,400,300,500)
        self.a_rectangle7 = QLS.Rectangle(0,400,99,200)

    def test_Create_Point(self):
        a_point = QLS.Point(1, (10,50))
    def test_rectangle(self):
        a_rectangle = QLS.Rectangle(0,0,100,100)



    def test_Rectangle_contains(self):
        self.assertTrue(self.a_rectangle.contains(self.a_point.getPoint()))
    def test_Rectangle_NOT_contains(self):
        self.assertFalse(self.a_rectangle.contains(self.a_point2.getPoint()))



    def test_Rectangles_intersect(self):
        self.assertFalse(self.a_rectangle.Notintersects(self.a_rectangle2))
    def test_Rectangles_NOT_intersect_left(self):
        self.assertTrue(self.a_rectangle.Notintersects(self.a_rectangle3))
    def test_Rectangles_NOT_intersect_right(self):
        self.assertTrue(self.a_rectangle.Notintersects(self.a_rectangle4))
    def test_Rectangles_NOT_intersect_up(self):
        self.assertTrue(self.a_rectangle.Notintersects(self.a_rectangle5))
    def test_Rectangles_NOT_intersect_down(self):
        self.assertTrue(self.a_rectangle.Notintersects(self.a_rectangle6))
    def test_Rectangles_NOT_intersect_botLeft(self):
        self.assertTrue(self.a_rectangle.Notintersects(self.a_rectangle7))
        

def testMain():
    unittest.main()








if __name__ == "__main__":
    ###############################################################
    #--------------------------------------------------------------
    # 1) Comment out one of the two lines below:
    #   Remove/add  either a '#' at the beginning of the line OR
    #   """    """
    # 2) Run this program/file

    # RUN MAIN PROGRAM
    QLS.MainInputs()
    # RUN TEST PROGRAM
    """testMain()"""




