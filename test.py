"""
Tests asssume you are running a local MySQL DB with root as user
and no password set. Will create test DB first time it's run and
reload the tables on every subsequent run.
"""
import os
import tests
import unittest
import flyingcow.db

suite = unittest.TestSuite()

# Find all the tests and add them to suite.
testdir = os.path.dirname(tests.__file__)
topdir = os.path.abspath(os.path.dirname(__file__))
for root, dirnames, filenames in os.walk(testdir):
    for filename in filenames:
        filepath = os.path.join(root, filename)
        relpath = filepath[len(topdir)+1:]
        
        if (filename == "__init__.py" or filename.endswith(".pyc")):
            continue
        
        if filename.endswith(".py"):
            modpath = relpath.replace(os.path.sep, ".")[:-3]
            module = __import__(modpath, None, None, [""])            
            suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))

# reset db schema / data.
db = flyingcow.db.register_connection(host='localhost', name='flyingcow_tests', user='root', password='')

runner = unittest.TextTestRunner()
runner.run(suite)
