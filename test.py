import unittest
from D1 import d1p1, d1p2
from D2 import d2p1, d2p2
from D3 import d3p1, d3p2
from D4 import d4p1, d4p2
from D5 import d5p1, d5p2
from D6 import d6p1, d6p2
from D7 import d7p1, d7p2
from D8 import d8p1, d8p2
from D9 import d9p1, d9p2
from D10 import d10p1, d10p2
from D11 import d11p1, d11p2
from D12 import d12p1, d12p2
from D13 import d13p1, d13p2


class TestD1(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d1p1(), 3198599)

    def test_p2(self):
        self.assertEqual(d1p2(), 4795042)


class TestD2(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d2p1(), 3790689)

    def test_p2(self):
        self.assertEqual(d2p2(), 6533)


class TestD3(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d3p1(), 529)

    def test_p2(self):
        self.assertEqual(d3p2(), 20386)


class TestD4(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d4p1(), 1625)

    def test_p2(self):
        self.assertEqual(d4p2(), 1111)


class TestD5(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d5p1(), 9025675)

    def test_p2(self):
        self.assertEqual(d5p2(), 11981754)


class TestD6(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d6p1(), 106065)

    def test_p2(self):
        self.assertEqual(d6p2(), 253)


class TestD7(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d7p1(), 422858)

    def test_p2(self):
        self.assertEqual(d7p2(), 14897241)


class TestD8(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d8p1(), 1584)

    def test_p2(self):
        self.assertEqual(d8p2(), 'KCGEC')


class TestD9(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d9p1(), 2494485073)

    def test_p2(self):
        self.assertEqual(d9p2(), 44997)


class TestD10(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d10p1(), 299)

    def test_p2(self):
        self.assertEqual(d10p2(), 1419)


class TestD11(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d11p1(), 1951)

    def test_p2(self):
        self.assertEqual(d11p2(), 'HKJBAHCR')


class TestD12(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d12p1(), 6490)

    def test_p2(self):
        self.assertEqual(d12p2(), 277068010964808)


class TestD13(unittest.TestCase):
    def test_p1(self):
        self.assertEqual(d13p1(), 200)

    def test_p2(self):
        self.assertEqual(d13p2(), 9803)


if __name__ == '__main__':
    unittest.main()
