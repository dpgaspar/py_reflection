class TreeDict(object):
    """
        A simple tree based on dicts
    """
    tree = None
    
    def __init__(self):
        self.tree = {}
        
    def set_node(self, key, tree = None):
        if tree is None: tree = self.tree
        if key not in tree:
            childs = {}
            tree[key] = childs
            return True
        return False
        
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
            print '|' + '-' * depth + '>', key
            if childs: self.debug(childs, depth +1)

    def print_map(self, tree = None, map_func = None, depth = 0):
        tree = tree or self.tree
        for key in tree:
            childs = tree.get(key)
            print '|' + '-' * depth + '>', map_func(key, depth)
            if childs: self.print_map(childs, map_func = map_func, depth = depth +1)

            
