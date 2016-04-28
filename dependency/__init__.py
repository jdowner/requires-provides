import functools
import weakref


class MissingRequirementError(Exception):
    def __init__(self, req):
        msg = "missing requirement: {}".format(req)
        super(MissingRequirementError, self).__init__(msg)


class Requirement(object):
    instances = weakref.WeakValueDictionary()

    def __new__(cls, name):
        if name in Requirement.instances:
            return Requirement.instances[name]

        obj = super(cls, Requirement).__new__(cls)
        setattr(obj, 'name', name)

        Requirement.instances[name] = obj

        return obj


class requires(object):
    def __init__(self, *args, **kwargs):
        self.requires = set(args)
        self.dynamic = kwargs.get('dynamic', False)

    def __call__(self, func, *args, **kwargs):
        @functools.wraps(func)
        def static_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        @functools.wraps(func)
        def dynamic_wrapper(*args, **kwargs):
            for req in self.requires:
                if req not in Requirement.instances:
                    raise MissingRequirementError(req)

            return func(*args, **kwargs)

        if self.dynamic:
            return dynamic_wrapper

        for req in self.requires:
            if req not in Requirement.instances:
                raise MissingRequirementError(req)

        return static_wrapper


class provides(object):
    def __init__(self, *args):
        self.properties = [Requirement(p) for p in args]

    def __call__(self, func, *args, **kwargs):
        @functools.wraps(func)
        def impl(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(impl, '__provides__', self)

        return impl

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return False
