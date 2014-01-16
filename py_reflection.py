import inspect
import sys
import os, pkgutil
import imp
import json
from treedict import TreeDict


class ClassNode(object):
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return self.value.__module__ + '.' + self.name
 
    def dump(self, depth):
        retstr = self.value.__module__ + '.' + self.name
        for i in self.value.__dict__:
            if hasattr(getattr(self.value,i), '__call__'):
                retstr = retstr + '\n' + ' ' * (depth+2) + i + '()'
        return retstr
        
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))


class BaseReflection(object):
    
    def __init__(self, obj_reflection):
        self.obj_reflection = obj_reflection

class Mix(object):
    
    e = 1
    
    def set_e(self, e):
        self.e = e

class PKGModuleRefletion(Mix, BaseReflection):

    def __init__(self, package_name):
        self.package_name = package_name
        self.class_tree = TreeDict()
        self.package = self.import_module(self.package_name)
        self.modules = self.get_modules()
        self.import_all(self.package)
        self.get_all_classes(self.package)
    
    def import_module(self, module_name):
        try:
            return __import__(module_name)
        except:
            print "import Error %s" % (module_name)
            return None
    
    def import_all(self, module, depth = 0):
        for imp, name, ispkg in self.get_modules(module):
            if ispkg: 
                package = self.import_module(module.__name__ + '.' + name)
                if hasattr(module, name):
                    self.import_all(getattr(module,name), depth + 1)
            else: 
                self.import_module(module.__name__ + '.' + name)
        
    def get_all_classes(self, module, depth = 0):
        modules = self.get_modules(module)
        if modules:
            for imp, name, ispkg in modules:
                if ispkg: 
                    if hasattr(module, name):
                        self.get_all_classes(getattr(module,name), depth + 1)
                else:
                    if hasattr(module, name):
                        for name, value in self.get_classes(getattr(module,name)):
                            self.add_class(name,value)
        for name, value in self.get_classes(module):
            self.add_class(name,value)

    
    def add_class(self, name, value, depth = 0):
        for parent in value.__bases__:
            self.add_class(parent.__name__,parent, depth + 1)
            self.class_tree.add_node(ClassNode(name, value),ClassNode(parent.__name__,parent))
        self.class_tree.add_node(ClassNode(name, value))
    
    def get_classes(self, module = None):
        module = module or self.package
        return [(a,b) for a,b in inspect.getmembers(module, inspect.isclass)]

    def get_modules(self, module = None):
        module = module or self.package
        if hasattr(module,'__path__'):
            return [(imp, name, ispkg) for (imp, name, ispkg) in pkgutil.iter_modules(module.__path__)]
        else: return []


cr = PKGModuleRefletion(sys.argv[1])
cr.class_tree.debug()
#cr.class_tree.print_map(map_func=ClassNode.dump)
