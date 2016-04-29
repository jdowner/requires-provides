==================================================
REQUIRES-PROVIDES
==================================================

This package provides a simple, flexible mechanism for specifying dependencies
among functions and classes in python.


.. image:: https://travis-ci.org/jdowner/requires-provides.svg?branch=master
    :target: https://travis-ci.org/jdowner/requires-provides


Installation
--------------------------------------------------

To install 'requires-provides' you can either use,

::

  $ sudo python setup.py install

or,

::

  $ sudo make install

This will install the python package 'dependency' to the standard location for
your system.


Usage
--------------------------------------------------

The basic idea is that classes or function can expressed whether require or
provide information that is necessary to fulfill some requirement. The
requirement is simply a string and can be thought of as a requirement tag. For
example, to create a class that fulfills the 'foo' requirement,

::

  # Specify a class that provides information to satisfy a requirement
  @dependency.provides('foo')
  class Foo(object):
      pass


A class that requires the 'foo' requirement to be fulfilled is expressed as,

::

  # Specify a class that requires information associated with a requirement
  @dependency.requires('foo')
  class Bar(object):
      pass


Class of functions can specify multiple provides or requires,

::

  @dependency.provides('foo', 'bar')
  def f():
      pass

  @dependency.provides('baz')
  def g():
      pass

  @dependency.requires('foo', 'bar', 'baz')
  def h():
      pass


When a requirement is unfulfilled an exception is raised,

::

  # If nothing provides 'foo', this function will raise a
  # MissingRequirementError when it is first declared.
  @dependency.requires('foo')
  def f():
      pass


If a requirement is dynamic and needs to be checked when a function is invoked
rather than when it is created, a dynamic flag can be set to provide this
behavior,

::

  # This requirement is not tested until the function is invoked
  @dependency.requires('foo', dynamic=True)
  def f():
      pass


If a requirement is only transiently fulfilled, a context manager may be used to
express this transience,

::

  @dependency.requires('foo', dynamic=True)
  def f():
      pass

  # This will succeed
  with dependency.provides('foo'):
    f()

  # This will raise a MissingRequirementException
  f()


And, of course, requires and provides can be mixed in a variety of ways,

::

  @dependency.requires('foo')
  @dependency.requires('bar', dynamic=True)
  @dependency.provides('baz')
  def f():
      pass


Dependencies
--------------------------------------------------

'requires-provides' currently depends on following packages (for testing),

* pep8
* tox
