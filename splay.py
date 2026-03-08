"""
Splay Tree implementation.

A splay tree is a self-adjusting binary search tree. After each access
operation (search, insert, or delete), the accessed node is moved to
the root through a sequence of tree rotations.

This adaptive behavior improves access time for recently or frequently
used elements, following the principle of locality of reference.

The tree supports the following operations:
- search
- insertion
- deletion
- splaying through Zig, Zig-Zig, and Zig-Zag rotations
"""

from __future__ import annotations
import json
from typing import List

verbose = False


# Node used in the splay tree
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

class SplayForest():
    def  __init__(self,
                  roots : None):
        self.roots = roots

    def newtree(self,treename):
        self.roots[treename] = None

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    def dump(self):
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.roots == None:
            dict_repr = {}
        else:
            dict_repr = {}
            for t in self.roots:
                if self.roots[t] is not None:
                    dict_repr[t] = _to_dict(self.roots[t])
        print(json.dumps(dict_repr,indent = 2))

    # Search:
    # Search for the key or the last node before we fall out of the tree.
    # Splay that node and record a list of the keys corresponding to the nodes
    # which experienced rotations, in the correct order.
    def search(self,treename: str,key:int):

        record = []
        root = self.roots[treename]
        
        if not root:
            return record 
        
        current_node = root
        result = None

        while current_node is not None:
            result = current_node
            record.append(result.key)  
            if key < current_node.key:
                current_node = current_node.leftchild
            elif key > current_node.key:
                current_node = current_node.rightchild
            else:  
                break

        self.splay(treename, result)

        return record  


    # Insert a new key and splay the last accessed node
    # The key is guaranteed to not be in the tree.
    # Call splay(x) and respond according to whether we get the IOP or IOS.
    def insert(self,treename:str,key:int):
        new_node = Node(key)

        root = self.roots[treename]

        if root is None:
            self.roots[treename] = new_node
            return

        current_node = root
        fall_out_node  = None

        while current_node is not None:
            fall_out_node = current_node
            if key < current_node.key:
                current_node = current_node.leftchild
            else:
                current_node = current_node.rightchild

        self.splay(treename,fall_out_node)

        root = self.roots[treename]

        if key < root.key:
            new_node.leftchild = root.leftchild
            new_node.rightchild = root
            if root.leftchild:
                root.leftchild.parent = new_node
            root.leftchild = None
            root.parent = new_node
        else:
            new_node.leftchild = root
            new_node.rightchild = root.rightchild
            if root.rightchild:
                root.rightchild.parent = new_node
            root.rightchild = None
            root.parent = new_node

        new_node.parent = None
        self.roots[treename] = new_node

    # Delete a key after splaying it to the root
    # The key is guarenteed to be in the tree.
    # Call splay(key) and then respond accordingly.
    # If key (now at the root) has two subtrees call splay(key) on the right one.
    def delete(self,treename:str,key:int):

        root = self.roots[treename]

        current_node = root
        result = None

        while current_node is not None:
            result = current_node
            if current_node.key < key:
                current_node = current_node.rightchild
            elif current_node.key > key:
                current_node = current_node.leftchild
            else:
                break

        self.splay(treename, result)      
        root = self.roots[treename]

        if root.leftchild and root.rightchild:
            ios_node = root.rightchild
            while ios_node.leftchild is not None:
                ios_node = ios_node.leftchild

            self.splay(treename, ios_node)
            
            ios_node.leftchild = root.leftchild
            if root.leftchild is not None:
                root.leftchild.parent = ios_node

            self.roots[treename] = ios_node
            ios_node.parent = None

        elif root.leftchild and not root.rightchild:
            self.roots[treename] = root.leftchild
            root.leftchild.parent = None

        elif root.rightchild and not root.leftchild :
            self.roots[treename] = root.rightchild
            root.rightchild.parent = None

        else:
            self.roots[treename] = None



    def splay(self, treename: str, node: Node):
        while node.parent is not None: 
            parent = node.parent
            g_parent = node.parent.parent

            if g_parent is None:
                if node == parent.leftchild:
                    self.rotation_right(treename, parent)
                elif node == parent.rightchild:
                    self.rotation_left(treename, parent)
            else:
                if node == parent.leftchild and parent == g_parent.leftchild:
                    self.rotation_right(treename, g_parent)
                    self.rotation_right(treename, parent)
                elif node == parent.rightchild and parent == g_parent.rightchild:
                    self.rotation_left(treename, g_parent)
                    self.rotation_left(treename, parent)
                elif node == parent.leftchild and parent == g_parent.rightchild:
                    self.rotation_right(treename, parent)
                    self.rotation_left(treename, g_parent)
                elif node == parent.rightchild and parent == g_parent.leftchild:
                    self.rotation_left(treename, parent)
                    self.rotation_right(treename, g_parent)


    def rotation_left(self,treename:str, node: Node,):
        
        start_node = node.rightchild
        if start_node is None:
            return

        node.rightchild = start_node.leftchild
        if start_node.leftchild:
            start_node.leftchild.parent = node

        start_node.leftchild = node
        start_node.parent = node.parent

        if node.parent:
            if node == node.parent.leftchild:
                node.parent.leftchild = start_node
            else:
                node.parent.rightchild = start_node
        else:
            self.roots[treename] = start_node
        node.parent = start_node


    def rotation_right(self,treename:str, node: Node):
        start_node = node.leftchild
        if start_node is None:
            return

        node.leftchild = start_node.rightchild
        if start_node.rightchild:
            start_node.rightchild.parent = node

        start_node.rightchild = node
        start_node.parent = node.parent

        if node.parent:
            if node == node.parent.leftchild:
                node.parent.leftchild = start_node
            else:
                node.parent.rightchild = start_node
        else:
            self.roots[treename] = start_node
        node.parent = start_node