import unittest

from normedtuple.core import normedtuple


# Top-level norm function
def top_level_norm(cls, x):
    "Top level norm function"
    return (x * 10,)


class NormFunctionScopes:

    def make_local_norm(self):
        def local_norm(cls, x, y):
            "Locally scoped norm"
            return (x - 1, y - 1)

        return local_norm


class TestQualnamePreservation(unittest.TestCase):

    def test_top_level_function_qualname(self):
        Decorated = normedtuple(top_level_norm)
        self.assertEqual(Decorated.__qualname__, top_level_norm.__qualname__)
        self.assertEqual(Decorated(2), (20,))
        self.assertTrue(Decorated.__qualname__.endswith("top_level_norm"))

    def test_nested_function_qualname(self):
        norm_func = NormFunctionScopes().make_local_norm()
        Decorated = normedtuple(norm_func)
        self.assertEqual(Decorated.__qualname__, norm_func.__qualname__)
        self.assertEqual(Decorated(3, 4), (2, 3))
        self.assertIn("local_norm", Decorated.__qualname__)
        self.assertIn("make_local_norm.<locals>", Decorated.__qualname__)

    def test_metadata_full_preservation(self):
        norm_func = NormFunctionScopes().make_local_norm()
        Decorated = normedtuple(norm_func)

        self.assertEqual(Decorated.__name__, norm_func.__name__)
        self.assertEqual(Decorated.__doc__, norm_func.__doc__)
        self.assertEqual(Decorated.__module__, norm_func.__module__)
        self.assertEqual(Decorated.__qualname__, norm_func.__qualname__)


if __name__ == "__main__":
    unittest.main()
