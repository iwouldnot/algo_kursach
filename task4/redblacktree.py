from node import Node


BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class RedBlackTree:
    # каждая нода имеет null-ноды как детей при инициализации, создаем один экземпляр такого объекта для удобства
    NIL_LEAF = Node(value=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # Используется для удаления и использует отношения бро с его родителем для определения типа поворота
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def add(self, value):
        if not self.root:
            self.root = Node(value, color=BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_dir = self._find_parent(value)
        if node_dir is None:
            return  # значение уже в дереве
        new_node = Node(value=value, color=RED, parent=parent, left=self.NIL_LEAF, right=self.NIL_LEAF)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    def remove(self, value):
        """
        Попытаемся получить ноду с 0 или 1 ребенком
        Или данная нода имеет 0 или 1 ребенка, или мы получим её наследника
        """
        node_to_remove = self.find_node(value)
        if node_to_remove is None:  # ноды нету в дереве
            return
        if node_to_remove.count_children() == 2:
            # найти in-order наследника и заменить его value
            # потом - удалить наследника
            successor = self._find_in_order_successor(node_to_remove)
            node_to_remove.value = successor.value  # присваиваем новый value
            node_to_remove = successor

        # нода имеет 0 или 1 ребенка
        self._remove(node_to_remove)
        self.count -= 1

    def find_node(self, value):
        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if value > root.value:
                return inner_find(root.right)
            elif value < root.value:
                return inner_find(root.left)
            else:
                return root

        found_node = inner_find(self.root)
        return found_node

    def contains(self, value) -> bool:
        """ Возвращает bool, показывающий, есть ли это значение в дереве или нет """
        return bool(self.find_node(value))

    def _remove(self, node):
        """
        Получает ноду с 0 или 1 ребенком (обычно это наследник)
        и удаляет его в соответствии с его цветом/детьми
        :param node: Нода с 0 или 1 ребенком
        """
        left_child = node.left
        right_child = node.right
        not_nil_child = left_child if left_child != self.NIL_LEAF else right_child
        if node == self.root:
            if not_nil_child != self.NIL_LEAF:
                # если мы удаляем корень и он имеет одного возможного ребенка, просто делаем этого ребенка корнем
                self.root = not_nil_child
                self.root.parent = None
                self.root.color = BLACK
            else:
                self.root = None
        elif node.color == RED:
            if not node.has_children():
                # Красная нода без детей, простейший случай
                self._remove_leaf(node)
            else:
                """
                Поскольку нода красная, у нее не может быть ребенка.
                Если она имеет ребенка, ей необходимо быть черной, но это бы означало,
                что черная высота должна быть больше на одной стороне, а это сделало бы наше дерево некорректным.
                """
                raise Exception('Unexpected behavior')
        else:  # нода ЧЕРНАЯ
            if right_child.has_children() or left_child.has_children():  # прост sanity check
                raise Exception('Красный ребенок черной ноды с 0 или 1 рбенком не может иметь детей, '
                                'иначе черная высота дерева становится некорректной!')
            if not_nil_child.color == RED:
                """
                Свапнуть значения с красным ребенком и удалить его (фактически, прост отлинковать его)
                Поскольку у ноды только один ребенок, мы можем быть уверенны, что нет нод ниже красного ребенка.
                """
                node.value = not_nil_child.value
                node.left = not_nil_child.left
                node.right = not_nil_child.right
            else:  # ЧЕРНЫЙ ребенок
                # мама мия, 6 кейсов :О
                self._remove_black_node(node)

    def _remove_leaf(self, leaf):
        """ Прост убирает листовую ноду, задавая родителю в качестве значения NIL_LEAF """
        if leaf.value >= leaf.parent.value:
            # в тех наркоманских случаях, когда они равны из-за свапа с наследником
            leaf.parent.right = self.NIL_LEAF
        else:
            leaf.parent.left = self.NIL_LEAF

    def _remove_black_node(self, node):
        """
        Проходим поочередно через каждый кейс рекурсивно, пока мы не достигнем конечного случая
        Останется одна листовая нода, которую можно удалить без последствий
        """
        self.__case_1(node)
        self._remove_leaf(node)

    def __case_1(self, node):
        """
        Кейс 1 наступает, когда есть двойная черная нода от корня
        Поскольку мы в корне, мы прост можем удалить её и уменьшить черную высоту всего дерева

            __|10B|__                  __10B__
           /         \      ==>       /       \
          9B         20B            9B        20B
        """
        if self.root == node:
            node.color = BLACK
            return
        self.__case_2(node)

    def __case_2(self, node):
        """
        Кейс 2 наступает, когда:
            родители ЧЕРНЫЕ
            бро КРАСНЫЙ
            дети бро - ЧЕРНЫЕ или NIL
        Нужно повернуть относительно бро

                         40B                                              60B
                        /   \       --КЕЙС 2 ПОВОРАЧИВАЕМ-->             /   \
                    |20B|   60R       ЛЕВЫЙ ПОВОРОТ                    40R   80B
        ЧЕРНЫЙ  20----^   /   \      БРО 60R                          /   \
                         50B    80B                                |20B|  50B
            (если бы направление бро было левым относительно его родителя, мы бы сделали ПРАВЫЙ ПОВОРОТ)
        Теперь родитель изначальной ноды КРАСНЫЙ,
        и мы можем применить кейс 4 или кейс 6
        """
        parent = node.parent
        sibling, direction = self._get_sibling(node)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(node)
        self.__case_3(node)

    def __case_3(self, node):
        """
        Кейс 3 удаления происходит, когда:
            родитель ЧЕРНЫЙ
            бро ЧЕРНЫЙ
            ребенок бро ЧЕРНЫЙ
        Тогда мы делаем бро КРАСНЫМ и проносим
        двойную черную ноду наверх

                            Родитель черный
               ___50B___    Бро черный                             ___50B___
              /         \   Ребенок бро черный                    /         \
           30B          80B        КЕЙС 3                       30B        |80B|  Продолжаем с остальными кейсами
          /   \        /   \        ==>                        /  \        /   \
        20B   35R    70B   |90B|<---УДАЛИТЬ                  20B  35R     70R   X
              /  \                                               /   \
            34B   37B                                          34B   37B
        """
        parent = node.parent
        sibling, _ = self._get_sibling(node)
        if (sibling.color == BLACK and parent.color == BLACK
           and sibling.left.color != RED and sibling.right.color != RED):
            # красим бро красным и проталкивают двойную черную ноду наверх
            # (вызываем кейсы снова для родителя)
            sibling.color = RED
            return self.__case_1(parent)  # поехали снова

        self.__case_4(node)

    def __case_4(self, node):
        """
        Если родитель красный и бро черный без красных детей,
        прост свапаем их цвета
        DB-двойной черный
                __10R__                   __10B__        Черная высота на левом поддереве увеличилась
               /       \                 /       \       Но с другой стороны из-за замены тоже
             DB        15B      ===>    X        15R     Последствий нету, все окич
                      /   \                     /   \
                    12B   17B                 12B   17B
        """
        parent = node.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(node)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # меняем цвета
                return  # конечный случай
        self.__case_5(node)

    def __case_5(self, node):
        """
        Кейс 5 - это поворот, который меняет ситуацию так, что мы можем применить кейс 6
        Если ближняя нода КРАСНАЯ и внешняя ЧЕРНАЯ или NIL, мы делаем левую/правую ротацию, в зависимости от ориентации
        Этот пример показывает случай, когда БЛИЖНЯЯ НОДА имеет направление СПРАВА

              ___50B___                                                    __50B__
             /         \                                                  /       \
           30B        |80B|  <-- Удвоенная черная                       35B      |80B|        Теперь тут применим
          /  \        /   \      Ближняя нода красная (35R)            /   \      /           кейс 6, поэтмоу
        20B  35R     70R   X     Внешняя - черная (20B)             30R    37B  70R           мы отсылаем ноду
            /   \                Мы делаем ЛЕВЫЙ ПОВОРОТ           /   \                      к нему
          34B  37B               от 35R (ближней ноды)           20B   34B
        """
        sibling, direction = self._get_sibling(node)
        closer_node = sibling.right if direction == 'L' else sibling.left
        outer_node = sibling.left if direction == 'L' else sibling.right
        if closer_node.color == RED and outer_node.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(node=None, parent=closer_node, grandfather=sibling)
            else:
                self._right_rotation(node=None, parent=closer_node, grandfather=sibling)
            closer_node.color = BLACK
            sibling.color = RED

        self.__case_6(node)

    def __case_6(self, node):
        """
        Для кейса 6 нужно:
            БРО должен быть ЧЕРНЫМ
            ВНЕШНЯЯ НОДА должна быть КРАСНОЙ
        Затем, выполняется правая/левая ротация на бро
        Ниже пример, когда направлеие бро - ЛЕВОЕ

                            Удвоенный черный
                    __50B__       |                               __35B__
                   /       \      |                              /       \
      БРОТАН --> 35B      |80B| <-                             30R       50R
                /   \      /                                  /   \     /   \
             30R    37B  70R   Внешняя нода RED            20B   34B 37B    80B
            /   \              Ближняя нода ни на что                       /
         20B   34B                 не влияет                              70R
                               Родитель ни на что
                                   не влияет
                               Так что фигачим правую ротацию на 35B
        """
        sibling, direction = self._get_sibling(node)
        outer_node = sibling.left if direction == 'L' else sibling.right

        def __case_6_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=sibling.parent)
            # new parent is sibling
            sibling.color = parent_color
            sibling.right.color = BLACK
            sibling.left.color = BLACK

        if sibling.color == BLACK and outer_node.color == RED:
            return __case_6_rotation(direction)  # terminating

        raise Exception('We should have ended here, something is wrong')

    def _try_rebalance(self, node):
        """
        Дается красная нода-потомок, определяется, нужно ли ее ребалансировать (красный ли предок)
        Если так, ребалансируем ноду
        """
        parent = node.parent
        value = node.value
        if (parent is None  # чёч? откуда он None вообще? в теории, не должно быть такого, но на всякий пожарный
           or parent.parent is None  # предок является корнем дерева
           or (node.color != RED or parent.color != RED)):  # нет нужды ребалансировать
            return
        grandfather = parent.parent
        node_dir = 'L' if parent.value > value else 'R'
        parent_dir = 'L' if grandfather.value > parent.value else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # поворот
            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(node=None, parent=node, grandfather=parent)
                # из-за предыдущей ротации, наша нода теперь родитель
                self._left_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(node=None, parent=node, grandfather=parent)
                # из-за предыдущей ротации, наша нода теперь родитель
                self._right_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("{} is not a valid direction!".format(general_direction))
        else:  # дядя - RED
            self._recolor(grandfather)

    def __update_parent(self, node, parent_old_child, new_parent):
        """
        Наша нода "меняется" местами со старым потомком
        Ноде присваивается новый родитель
        Если new_parent is None, значит, нода становится корнем дерева
        """
        node.parent = new_parent
        if new_parent:
            # Определяем старое положение потомка, чтобы закинуть сюда ноду
            if new_parent.value > parent_old_child.value:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def _right_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right  # сохраняем старые правые значения
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _left_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  # сохраняем старые левые значения
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def _find_parent(self, value):
        """ Ищет место для нового значения в бинарном дереве """
        def inner_find(parent):
            """
            Возвращает подходящую родительскую ноу для нашей новой ноды и сторону, на которой она должна быть
            """
            if value == parent.value:
                return None, None
            elif parent.value < value:
                if parent.right.color == NIL:  # больше некуда идти
                    return parent, 'R'
                return inner_find(parent.right)
            elif value < parent.value:
                if parent.left.color == NIL:  # больше некуда идти
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def _find_in_order_successor(self, node):
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NIL_LEAF:
            return right_node
        while left_node.left != self.NIL_LEAF:
            left_node = left_node.left
        return left_node

    @staticmethod
    def _get_sibling(node):
        """
        Возвращает родного брозера ноды и сторону, на которой нода находится
        Например:

            20 (A)
           /     \
        15(B)    25(C)

        _get_sibling(25(C)) => 15(B), 'L'
        """
        parent = node.parent
        if node.value >= parent.value:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction
