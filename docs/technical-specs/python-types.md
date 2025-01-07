Mojo/Manual/Python/Python types
Python types
When calling Python methods, Mojo needs to convert back and forth between native Python objects and native Mojo objects. Most of these conversions happen automatically, but there are a number of cases that Mojo doesn't handle yet. In these cases you may need to do an explicit conversion, or call an extra method.

Mojo types in Python

Mojo primitive types implicitly convert into Python objects. Today we support integers, floats, booleans, strings, tuples, and ListLiteral instances (described below in Mojo wrapper objects).

To demonstrate, the following example dynamically creates an in-memory Python module named py_utils containing a type_printer() function, which simply prints the type of a given value. Then you can see how different Mojo values convert into corresponding Python types.

from python import Python

def main():
    py_module = """
def type_printer(value):
    print(type(value))
"""
    py_utils = Python.evaluate(py_module, file=True, name="py_utils")

    py_utils.type_printer(4)
    py_utils.type_printer(3.14)
    py_utils.type_printer(("Mojo", True))

<class 'int'>
<class 'float'>
<class 'tuple'>
Python types in Mojo

You can also use Python objects from Mojo. For example, Mojo's Dict and List types don't natively support heterogeneous collections. One alternative is to use a Python dictionary or list.

For example, to create a Python dictionary, use the Python.dict() method:

from python import Python

def main():
    py_dict = Python.dict()
    py_dict["item_name"] = "whizbang"
    py_dict["price"] = 11.75
    py_dict["inventory"] = 100
    print(py_dict)

{'item_name': 'whizbang', 'price': 11.75, 'inventory': 100}
Mojo wrapper objects

When you use Python objects in your Mojo code, Mojo adds the PythonObject wrapper around the Python object. This object exposes a number of common double underscore methods (dunder methods) like __getitem__() and __getattr__(), passing them through to the underlying Python object.

You can explicitly create a wrapped Python object by initializing a PythonObject with a Mojo literal. Most of the time, you can treat the wrapped object just like you'd treat it in Python. You can use dot-notation to access attributes and call methods, and use the [] operator to access an item in a sequence. For example:

from python import PythonObject

def main():
    var py_list: PythonObject = ["cat", 2, 3.14159, 4]  # A ListLiteral
    n = py_list[2]
    print("n =", n)
    py_list.append(5)
    py_list[0] = "aardvark"
    print(py_list)

n = 3.14159
['aardvark', 2, 3.14159, 4, 5]
In the example above, ["cat", 2, 3.14159, 4] is an instance of ListLiteral, which supports lists of heterogeneous values. The ListLiteral type is intended only for Python interoperability, and it is not compatible with the native Mojo List type. For example, the following line results in a compilation error:
var mojo_list: List[Int] = [1, 2, 3, 4]

error: cannot implicitly convert 'ListLiteral[Int, Int, Int, Int]' value to 'List[Int]'
var mojo_list: List[Int] = [1, 2, 3, 4]
                           ^~~~~~~~~~~~
If you want to construct a Python type that doesn't have a literal Mojo equivalent, you can also use the Python.evaluate() method. For example, to create a Python set:

from python import Python

def main():
    var py_set = Python.evaluate('{2, 3, 2, 7, 11, 3}')
    num_items = len(py_set)
    print(num_items, "items in the set.")
    contained = 7 in py_set
    print("Is 7 in the set:", contained)

4 items in the set.
Is 7 in the set: True
Some Mojo APIs handle PythonObject just fine, but sometimes you'll need to explicitly convert a Python value into a native Mojo value.

Currently PythonObject conforms to the Intable, Stringable, and Boolable traits, which means you can convert Python values to Mojo Int, String, and Bool types using the built-in int(), str(), and bool() functions, and print Python values using the built-in print() function.

PythonObject also provides the to_float64() for converting to a Mojo floating point value.

var i: Int = int(py_int)
var s: String = str(py_string)
var b: Bool = bool(py_bool)
var f: Float64 = py_float.to_float64()

Comparing Python types in Mojo

You can use Python objects in Mojo comparison expressions, and the Mojo is operator also works to compare the identity of two Python objects. Python values like False and None evaluate as false in Mojo boolean expressions as well.

If you need to know the type of the underlying Python object, you can use the Python.type() method, which is equivalent to the Python type() builtin. You can test if a Python object is of a particular type by performing an identity comparison against the type as shown below:

from python import Python
from python import PythonObject

def main():
    var value1: PythonObject = 3.7
    value2 = Python.evaluate("10/3")

    # Compare values
    print("Is value1 greater than 3:", value1 > 3)
    print("Is value1 greater than value2:", value1 > value2)

    # Compare identities
    value3 = value2
    print("value1 is value2:", value1 is value2)
    print("value2 is value3:", value2 is value3)

    # Compare types
    py_float_type = Python.evaluate("float")
    print("Python float type:", py_float_type)
    print("value1 type:", Python.type(value1))
    print("Is value1 a Python float:", Python.type(value1) is py_float_type)

Is value1 greater than 3: True
Is value1 greater than value2: True
value1 is value2: False
value2 is value3: True
Python float type: <class 'float'>
value1 type: <class 'float'>
Is value1 a Python float: True