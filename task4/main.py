from autoservice import Autoservice
from redblacktree import RedBlackTree, RED, BLACK, Node
NIL_LEAF = RedBlackTree.NIL_LEAF


def main():
    rb_tree = RedBlackTree()

    # корень
    node_10_value = Autoservice(10, 'Переделкино', 'Вася Пупкин', 'Омск')
    root = Node(value=node_10_value, color=BLACK, parent=None, left=NIL_LEAF, right=NIL_LEAF)
    node_10 = root

    # левое поддерево
    node_5_value = Autoservice(5, 'Сломай меня полностью', 'Иннокентий Пересядько', 'Якутск')
    node_5 = Node(value=node_5_value, color=BLACK, parent=root, left=NIL_LEAF, right=NIL_LEAF)

    # правое поддерево
    node_20_value = Autoservice(20, 'Загони под шины', 'Яков Явенчучечков', 'Ханты-Мансийск')
    node_20 = Node(value=node_20_value, color=RED, parent=root, left=NIL_LEAF, right=NIL_LEAF)
    node_15_value = Autoservice(15, 'Вест Коуст Кастомс', 'Евакий Иксзибитов', 'Бирюлёво')
    node_15 = Node(value=node_15_value, color=BLACK, parent=node_20, left=NIL_LEAF, right=NIL_LEAF)
    node_25_value = Autoservice(25, 'Подкуй братуху', 'Каракантанбек Изумнетралитанаев', 'Владивосток')
    node_25 = Node(value=node_25_value, color=BLACK, parent=node_20, left=NIL_LEAF, right=NIL_LEAF)
    node_20.left = node_15
    node_20.right = node_25

    node_12_value = Autoservice(12, 'Железный сивый мерин', 'Эщкере Капиталистов', 'Староперуново')
    node_12 = Node(value=node_12_value, color=RED, parent=node_15, left=NIL_LEAF, right=NIL_LEAF)
    node_17_value = Autoservice(17, 'Вах Какой Машына', 'Джамшут Равшанов', 'Перезауехово')
    node_17 = Node(value=node_17_value, color=RED, parent=node_15, left=NIL_LEAF, right=NIL_LEAF)
    node_15.left = node_12
    node_15.right = node_17

    root.left = node_5
    root.right = node_20
    rb_tree.root = root

    node_19_value = Autoservice(19, 'На созвоне & вопросики порешаем & тоси-боси', 'Капитан Глазозоркость', 'Готтэм')

    print('Before:\n' + '-' * 80)
    for i in list(rb_tree):
        print(i)

    rb_tree.add(node_19_value)

    """
                ____10B____                           ____10B____
               5B      __20R__                       5B      __20R__
                  __15B__     25B   -- КРАСИМ В -->      __15R__    25B
               12R      17R                           12B      17B
               добавляем-->19R                                   19R

Общее
направление:                   ____10B____
   LR=>RL                   5B         ___15R___
правая ротация                       12B      __20R__
                                            17B      25B
                                              19R


                                 _____15B_____
    Левая ротация к           10R           __20R__
                            5B  12B       17B      25B
                                            19R
    """

    print('After:\n' + '-' * 80)
    for i in list(rb_tree):
        print(i)

    print('Trying to find \n{}\n in tree: \n{}'.format(node_17_value, rb_tree.find_node(node_17_value)))
    print()
    print('Is \n{}\n in tree? {}'.format(node_17_value, rb_tree.contains(node_17_value)))

    print('Tree root has children: {}'.format(rb_tree.root.has_children()))
    print('Tree root has {} children'.format(rb_tree.root.count_children()))

    values = [
        node_10_value,
        node_5_value,
        node_20_value,
        node_15_value,
        node_25_value,
        node_12_value,
        node_17_value
    ]

    print('-' * 80)
    rb_tree = RedBlackTree()
    for value in values:
        rb_tree.add(value)
        for i in list(rb_tree):
            print(i)
        print('-' * 80)

    print('-' * 80)
    for value in values:
        for i in list(rb_tree):
            print(i)
        rb_tree.remove(value)
        print('-' * 80)

if __name__ == '__main__':
    main()