import inspect
import sys
import os, pkgutil
import imp
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')


class TreeDict(object):
    
    tree = None
    
    def __init__(self):
        self.tree = {}
        
    def set_node(self, key, tree = None):
        if tree is None: tree = self.tree
        childs = {}
        tree[key] = childs
        return True
        
    def add_node(self, key, parent_key = None, tree = None, depth = 0, flag = False):
        if tree is None: tree = self.tree
        if parent_key:
            for _key in tree:
                if _key == parent_key:
                    return self.set_node(key, tree.get(_key))
                else: 
                    flag = self.add_node(key, parent_key, tree.get(_key), depth + 1, flag)
            return flag
        else:
            return self.set_node(key, tree)
    
    def debug(self, tree = None, depth = 0):
        tree = tree or self.tree
        for key in tree:
            childs = tree.get(key)
            print '-' * depth, key
            if childs: self.debug(childs, depth +1)



class ClassReflet(object):

    def __init__(self, package_name):
        self.package_name = package_name
        self.package = self.import_module(self.package_name)
        self.modules = self.get_modules()
        self.class_tree = TreeDict()
        self.import_all(self.package)
        self.get_all_classes(self.package)
        
    
    def import_module(self, module_name):
        print "importing: %s" % (module_name)
        return __import__(module_name)
    
    def import_all(self, module, depth = 0):
        for imp, name, ispkg in self.get_modules(module):
            if ispkg: 
                package = self.import_module(module.__name__ + '.' + name)
                self.import_all(getattr(module,name), depth + 1)
            else: 
                self.import_module(module.__name__ + '.' + name)
        
    def get_all_classes(self, module, depth = 0):
        for imp, name, ispkg in self.get_modules(module):
            if ispkg: 
                self.get_all_classes(getattr(module,name), depth + 1)
            else:
                for name, value in self.get_classes(getattr(module,name)):
                    self.add_class(name,value)
        for name, value in self.get_classes(module):
            self.add_class(name,value)
        
    def add_class(self, name, value):
        for parent in value.__bases__:
            if not self.class_tree.add_node((name, value),(parent.__name__,parent)):
                self.add_class(parent.__name__,parent)
            else: return
        self.class_tree.add_node((name, value))
        
    def get_classes(self, module = None):
        module = module or self.package
        return [(a,b) for a,b in inspect.getmembers(module, inspect.isclass)]

    def get_modules(self, module = None):
        module = module or self.package
        return [(imp, name, ispkg) for (imp, name, ispkg) in pkgutil.iter_modules(module.__path__)]



        
def print_class_tree(tree, indent=-1):
    if isinstance(tree, list):
        for node in tree:
            print_class_tree(node, indent+1)
    else:
        print '  ' * indent, tree[0].__name__
    return


def show_class_tree(a):
	print_class_tree(inspect.getclasstree(get_classes(a)))

cr = ClassReflet('flask_appbuilder')	
cr.class_tree.debug()

t = TreeDict()
print t.add_node('A')
print t.add_node('B')
print t.add_node('C')
print t.add_node('CC','C')
print t.add_node('BB','B')
print t.add_node('BBB','BB')
print t.add_node('BBBB','BBB')
print t.add_node('AA','A')
print t.add_node('CCC','CC')
print t.add_node('ZZ','ZZ')
print t.add_node('AA')
t.debug()
