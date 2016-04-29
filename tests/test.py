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

    def test_multiple_requirements(self):
        @dependency.provides('test-req-A')
        class TestClassA(object):
            pass

        @dependency.provides('test-req-B')
        class TestClassB(object):
            pass

        @dependency.requires('test-req-A', 'test-req-B')
        class TestClassB(object):
            pass

        @dependency.provides('test-req-func-A')
        def funcA():
            pass

        @dependency.provides('test-req-func-B')
        def funcB():
            pass

        @dependency.requires('test-req-func-A', 'test-req-func-B')
        def funcC():
            pass

    def test_mixed_requirements(self):
        @dependency.provides('test-req-A')
        def funcA():
            pass

        @dependency.provides('test-req-B')
        @dependency.requires('test-req-A')
        def funcB():
            pass

        @dependency.requires('test-req-A', 'test-req-B')
        def funcC():
            pass

        @dependency.requires('test-req-A', 'test-req-B')
        @dependency.requires('test-req-C', dynamic=True)
        def funcD():
            pass

        with self.assertRaises(dependency.MissingRequirementError):
            funcD()

        with dependency.provides('test-req-C'):
            funcD()

    def test_multiple_provision(self):
        @dependency.provides('test-req-A')
        def funcA():
            pass

        with self.assertRaises(dependency.MissingRequirementError):
            @dependency.requires('test-req-A', 'test-req-B')
            def funcB():
                pass

        with dependency.provides('test-req-A', 'test-req-B'):
            @dependency.requires('test-req-A', 'test-req-B')
            def funcC():
                pass

        @dependency.requires('test-req-A')
        def funcD():
            pass

        with self.assertRaises(dependency.MissingRequirementError):
            @dependency.requires('test-req-B')
            def funcE():
                pass
