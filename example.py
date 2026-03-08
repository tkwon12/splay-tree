from splay import SplayForest

forest = SplayForest({})
forest.newtree("main")

forest.insert("main", 10)
forest.insert("main", 5)
forest.insert("main", 15)
forest.insert("main", 7)

print("After inserts:")
forest.dump()

print("Search path:", forest.search("main", 7))
print("After splaying 7:")
forest.dump()

forest.delete("main", 10)
print("After deleting 10:")
forest.dump()