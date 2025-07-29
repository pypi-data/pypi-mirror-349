import unittest

import staticclasses


class Foo(staticclasses.staticclass): ...


class TestFoo(unittest.TestCase):
    def test_foo(self):
        error = None
        try:
            Foo()
        except TypeError as e:
            error = e
        self.assertNotEqual(error, None)


if __name__ == "__main__":
    unittest.main()
