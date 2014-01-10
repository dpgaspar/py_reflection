import inspect
import sys
import os, pkgutil
import imp
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

import flask.ext.appbuilder
from flask.ext.appbuilder import views, filters


def get_modules(p):
	pkgpath = os.path.dirname(p.__file__)
	return [a for a, name, b in pkgutil.iter_modules([pkgpath])]

def get_classes(a):
	return [b for a,b in inspect.getmembers(a, inspect.isclass)]

def get_current_classes():
	return [b for a,b in inspect.getmembers(sys.modules[__name__], inspect.isclass)]

def print_class_tree(tree, indent=-1):
    if isinstance(tree, list):
        for node in tree:
            print_class_tree(node, indent+1)
    else:
        print '  ' * indent, tree[0].__name__
    return


def show_class_tree(a):
	print_class_tree(inspect.getclasstree(get_classes(a)))

print "-------------- VIEWS ----------------"
show_class_tree(views)
print "-------------- FILTERS ----------------"
show_class_tree(filters)
print "------------- PACKAGE CONTENT --------"
for m in get_modules(flask.ext.appbuilder):
	print m.__module__
	
