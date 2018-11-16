from measure import CCodeParser
import unittest

class TestCCodeParser(unittest.TestCase):

    def test_if_a(self):
        ccode = 'if (a) { }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(1, parser.acyc())
        self.assertEqual(2, parser.cabe())

    def test_if_ab(self):
        ccode = 'if (a && b) { }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(3, parser.acyc())
        self.assertEqual(3, parser.cabe())

    def test_if_c(self):
        ccode = 'if (a && (b || c)) { }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(6, parser.acyc()) 
        self.assertEqual(4, parser.cabe()) 

    def test_for(self):
        ccode = 'for (int i; i<=9; i++) { }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(1, parser.acyc())
        self.assertEqual(2, parser.cabe())

    def test_while(self):
        ccode = 'while (i<=9) { }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(1, parser.acyc())
        self.assertEqual(2, parser.cabe())

    def test_nesting1(self):
        ccode = 'if (a && (b || c)) { if (d) { } }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(10, parser.acyc()) 
        self.assertEqual(5, parser.cabe()) 

    def test_nesting2(self):
        ccode = 'if (a && (b || c)) { if (d) { } if (e) {} }'
        parser = CCodeParser(ccode)
        parser.parse()
        self.assertEqual(14, parser.acyc()) 
        self.assertEqual(6, parser.cabe()) 

    def test_nesting3(self):
        ccode = '{ if (a) { } if (b) { } if (c) { } }'
        parser = CCodeParser(ccode)
        parser.parse()
        non = parser.acyc()

        ccode = '{ if (a) { if (b) { if (c) { } } } }'
        parser = CCodeParser(ccode)
        parser.parse()
        nested = parser.acyc()

        self.assertEqual(True, nested > non) 
        self.assertEqual(True, nested > parser.cabe()) 

    def test_folding(self):
        ccode = '{ if (a && b && c) { if (d) { } } }'
        parser = CCodeParser(ccode)
        parser.parse()
        folded = parser.acyc()

        ccode = '{ if (a) { if (b) { if (c) { if (d) { } } } } }'
        parser = CCodeParser(ccode)
        parser.parse()
        nested = parser.acyc()

        self.assertEqual(nested, folded) 

    def test_scopes(self):
        ccode = '{if (a) {}} {if (b) {}}'
        parser = CCodeParser(ccode)
        parser.parse()
        n = parser.acyc()
        self.assertEqual(2, n) 

    def test_scopes2(self):
        ccode = '{if (a) {}} {if (b) {}}'
        parser = CCodeParser(ccode)
        scopes = parser.parse()
        n = parser.acyc()
        self.assertEqual(2, len(scopes)) 


if __name__ == '__main__':
    unittest.main()
