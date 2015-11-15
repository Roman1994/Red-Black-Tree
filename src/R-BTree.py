class RBT :

  # 1. Все узлы либо красные, либо черные #
  # 2. Корень всегда черный               #
  # 3. Все листья(NIL) - черные           #
  # 4. Потомки красного узла - черные     #
  # 5. Всякий простой путь от данного     #
  # узла до листа содержит одинаковое     #
  # число черных узлов                    #

  count    = 0
  root     = None
  typeTree = None
  NIL      = None

  def __init__(self, item, parent=None) :
    self.subroot = item
    # цвет вершины Fasle-черный, True-красный #
    self.color   = False
    self.left    = None
    self.right   = None
    self.parent  = parent
    if self.subroot != None :
      RBT.count += 1
    if RBT.count == 1 :
      RBT.root = self
      RBT.typeTree = type(self.subroot)
      self.color = False

  def insert(self, key) :
    temp = None
    preCurrent = RBT.NIL
    current    = RBT.root
    if type(key) == RBT.typeTree :
      while current != RBT.NIL :
        preCurrent = current
        if key < current.subroot :
          if current.left == None :
            temp = RBT(key, current)
            current.left = temp
            # новая вершина окрашивается в красный #
            temp.color = True
            break
          else : current = current.left
        else :
          if current.right == None :
            temp = RBT(key, current)
            current.right = temp
            temp.color = True
            break
          else : current = current.right
      self.fixup(temp)
    else : print('error')

  def fixup(self, node) :
    self.__insertCase1(node)

  # если текущий узел-корень    #
  # его цвет обязательно черный #
  def __insertCase1(self, node) :
    print('case1')
    if node == RBT.root :
      node.color = False
    else : self.__insertCase2(node)
  # если предок текущего узла черный #
  def __insertCase2(self, node) :
    print('case2')
    if node.parent.color == False :
      return
    else : self.__insertCase3(node)
  # если родитель и дядя-красные, перекрасить в черный   #
  # тогда дедушка станет красным                         #
  # Но, если, дедушка-корень,или отец дедушки красный,   #
  # то он не может быть красным                          #
  def __insertCase3(self, node) :
    print('case3')
    uncle = self.__uncle(node)
    grandP = self.__grandparent(node)
    if (uncle != None) and         \
       (uncle.color == True) and   \
       (node.parent.color == True) :
      node.parent.color = False
      uncle.color = False
      grandP.color = True
      self.__insertCase1(grandP)
    else : self.__insertCase4(node)
  # родитель узла является красным, но дядя черный  #
  # Текущий узел - правы потомок, а его предок -    #
  # левый потомок своего предка                     #
  # В этом случае применить поворот дерева, который #
  # поменяет роли текущей вершины и его предка      #
  def __insertCase4(self, node) :
    print('case4')
    grandP = self.__grandparent(node)
    if (node == node.parent.right) and \
       (node.parent == grandP.left)    :
      self.__leftRotate(node)
      # node = node.left
    elif (node == node.parent.left) and \
         (node.parent == grandP.right)  :
      self.__rightRotate(node)
      # node = node.right
    self.__insertCase5(node)
  # Родитель является красным, но дядя - черный,  #
  # текущий узел - левый потомок предка, а предок #
  # левый потомок дедушки                         #
  # Выполнить поворот дерева на дедушку           #
  def __insertCase5(self, node) :
    print('case5')
    grandP = self.__grandparent(node)
    node.parent.color = False
    grandP.color = True
    if (node == node.parent.left) and \
       (node.parent == grandP.left) :
      self.__rightRotate(grandP)
    else :
      self.__leftRotate(grandP)

  def __leftRotate(self, oldRoot) :
    if oldRoot.right != None :
      newSubroot = oldRoot.right
      oldRoot.right = newSubroot.left
      if newSubroot.left != None :
        newSubroot.parent.left = oldRoot
      newSubroot.parent = oldRoot.parent
      if oldRoot.parent == None :
        RBT.root = newSubroot
      elif oldRoot == oldRoot.parent.left :
        oldRoot.parent.left = newSubroot
      else :
        oldRoot.parent.right = newSubroot
      newSubroot.left = oldRoot
      oldRoot.parent = newSubroot
  def __rightRotate(self, oldRoot) :
    if oldRoot.left != None :
      newSubroot = oldRoot.left
      oldRoot.left = newSubroot.right
      if newSubroot.right != None :
        newSubroot.right.parent = oldRoot
      newSubroot.parent = oldRoot.parent
      if oldRoot.parent == None :
        RBT.root = newSubroot
      elif oldRoot == oldRoot.parent.left :
        oldRoot.parent.left = newSubroot
      else : oldRoot.parent.right = newSubroot
      newSubroot.right = oldRoot
      oldRoot.parent = newSubroot

  def __grandparent(self, currNode) :
    if currNode != None and currNode.parent != None :
      return currNode.parent.parent
    else :
      return None
  def __uncle(self, currNode) :
    grandP = self.__grandparent(currNode)
    if grandP == None :
      return None
    if currNode.parent == grandP.left :
      return grandP.right
    else :
      return grandP.left

  @staticmethod
  def summa(tree) :
    if tree.left == None and tree.right == None :
      return tree.subroot
    elif tree.left == None and tree.right != None :
      return tree.subroot + tree.summa(tree.right)
    elif tree.left != None and tree.right == None :
      return tree.subroot + tree.summa(tree.left)
    else :
      return tree.subroot +          \
             tree.summa(tree.left) + \
             tree.summa(tree.right)

  @staticmethod
  def preorder(tree) :
    if tree :
      print(repr((tree.subroot, 'Red' if tree.color else 'Black')), end=' ')
      RBT.preorder(tree.left)
      RBT.preorder(tree.right)
  @staticmethod
  def inorder(tree) :
    if tree :
      RBT.inorder(tree.left)
      print(repr((tree.subroot, 'Red' if tree.color else 'Black')), end=' ')
      RBT.inorder(tree.right)
  @staticmethod
  def postorder(tree) :
    if tree :
      RBT.postorder(tree.left)
      RBT.postorder(tree.right)
      print(repr((tree.subroot, 'Red' if tree.color else 'Black')), end=' ')