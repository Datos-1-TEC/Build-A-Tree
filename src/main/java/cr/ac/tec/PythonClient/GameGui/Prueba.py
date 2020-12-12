from drawnTree import *
a = AVLTree()
a = BTree()


a.insert(1)

c = drawnTree(a, "AVL Tree") #Debe declarase después de insertar al menos un nodo

a.insert(2)
a.insert(0)
a.insert(-1)
c.update(a)
print(c.tree.rootNode.left.height)

#c.myfunc()

'''
a.insert(0)
print('Updating.......')
c.update(a)

a.insert(15)
a.insert(20)
a.insert(21)
a.insert(14)


c.update(a)
print(c.tree.rootNode.right.right.order)
print(c.tree.rootNode.right.right.depth)

#c.drawTree(a, "Sketit")
print("Updated!")
'''
