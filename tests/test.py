import unittest

import dependency


class TestRequiresProvides(unittest.TestCase):
    def test_provides(self):
        self.assertNotIn('test-req', dependency.Requirement.instances)

        @dependency.provides('test-req')
        class TestClass(object):
            pass

        self.assertIn('test-req', dependency.Requirement.instances)

    def test_context_provides(self):
        self.assertNotIn('test-req', dependency.Requirement.instances)

        with dependency.provides('test-req'):
            self.assertIn('test-req', dependency.Requirement.instances)

    def test_static_requires(self):
        with self.assertRaises(dependency.MissingRequirementError):
            @dependency.requires('test-req')
            class TestClassA(object):
                pass

        with self.assertRaises(dependency.MissingRequirementError):
            @dependency.requires('test-req')
            def test_funcA():
                pass

        with dependency.provides('test-req'):
            @dependency.requires('test-req')
            class TestClassB(object):
                pass

            @dependency.requires('test-req')
            def test_funcB():
                pass

    def test_dynamic_requires(self):
        class TestClass(object):
            @dependency.requires('test-req', dynamic=True)
            def func(self):
                pass

        @dependency.requires('test-req', dynamic=True)
        def test_func():
            pass

        obj = TestClass()

        with dependency.provides('test-req'):
            obj.func()
            test_func()

        with self.assertRaises(dependency.MissingRequirementError):
            obj.func()

        with self.assertRaises(dependency.MissingRequirementError):
            test_func()
