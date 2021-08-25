
import unittest
from modles import *
class TestVideo(unittest.TestCase):
    def test_init(self):
        v = Video('Avatar','2010',True)
        self.assertEqual(v.title,'Avatar')
        self.assertEqual(v.year,'2010')
        self.assertTrue(v.availability)
        self.assertTrue(isinstance(v.id,int))
        self.assertEqual(v.currentCustomer,None)
        self.assertEqual(v.history,[])
    def test_showDetail(self):
        v = Video('Avatar','2010',True)
        self.assertEqual(v.showDetail(),'Avatar 2010 Available')
        v = Video('Avatar','2010',False)
        self.assertEqual(v.showDetail(),'Avatar 2010 Not Available')
    
    def test_setRenting(self):
        vt = Video('Avatar','2010',True)
        c = Customer('Jack','Rolleston')
        vt.setRenting(c)
        self.assertEqual(vt.currentCustomer,c)
        self.assertFalse(vt.availability)
        vf = Video('Avatar','2010',False)
        with self.assertRaises( VideoError):
            vf.setRenting(c)
    def test_checkRentalRecord(self):
        v = Video('Avatar','2010',True)
        cTrue = Customer('Jack','Rolleston')
        cFalse = Customer('Mark','Lincoln')
        v.setRenting(cTrue)
        self.assertTrue(v.checkRentalRecord(cTrue))
        self.assertFalse(v.checkRentalRecord(cFalse))
    def test_setReturning(self):
        v = Video('Avatar','2010',True)
        cTrue = Customer('Jack','Rolleston')
        cFalse = Customer('Mark','Lincoln')
        v.setRenting(cTrue)
        v.setReturning(cTrue)
        self.assertIsNone(v.currentCustomer)
        self.assertTrue(cTrue in v.history)
        self.assertTrue(v.availability)
        with self.assertRaises(VideoError):
            v.setRenting(cTrue)
            v.setReturning(cFalse)

class TestCustomer(unittest.TestCase):
    def test_init(self):
        c = Customer('Jack','Rolleston')
        self.assertTrue(isinstance(c.id,int))
        self.assertEqual(c.name,'Jack')
        self.assertEqual(c.city,'Rolleston')
        self.assertEqual(c.payment,0.0)
        self.assertEqual(c.currentVideos,[])
        self.assertEqual(c.history,[])
    def test_setRenting(self):
        c = Customer('Jack','Rolleston')
        v1 = Video('Avatar','2010')
        v2 = Video('The Dark Knight', '2008')
        c.setRenting(v1)
        self.assertTrue(c.checkRentalRecord(v1))
        self.assertFalse(c.checkRentalRecord(v2))
        self.assertEqual(c.currentVideos,[v1])
        self.assertEqual(c.payment,2)
        with self.assertRaises(CustomerError):
            c.setRenting(v1)
            c.setRenting(v1)

    def test_setReturning(self):
        c = Customer('Jack','Rolleston')
        vTrue = Video('Avatar','2010')
        vFalse = Video('The Dark Knight', '2008')
        c.setRenting(vTrue)
        c.setReturning(vTrue)
        self.assertFalse(vTrue in c.currentVideos)
        self.assertTrue(vTrue in c.history)
        with self.assertRaises(CustomerError):
            c.setRenting(vTrue)
            c.setReturning(vFalse)