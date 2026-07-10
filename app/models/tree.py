from collections import deque


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Determines whether two binary tree are equals.
# @param root1: The root of a binary tree.
# @param root2: The root of a binary tree.
# @return: True if the two binary trees are equals, false otherwise.
def is_same_tree(root1, root2):
    q1 = deque([root1])
    q2 = deque([root2])

    while q1 and q2:
        node1, node2 = q1.popleft(), q2.popleft()

        if node1 == None and node2 == None:
            continue

        elif node1 == None or node2 == None:
            return False

        elif node1.value != node2.value:
            return False

        q1.append(node1.left)

        q1.append(node1.right)

        q2.append(node2.left)

        q2.append(node2.right)

    return True


# Traverses the binary tree level by level.
# @param root: The root node of the binary tree.
# @return: A stack containing the nodes in the order they are visited during traversal.
def level_order_traversal(root):
    q = deque([root])
    stack = []

    while q:
        q_lenght = len(q)

        for _ in range(q_lenght):
            node = q.popleft()
            stack.append(node)

            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

    return stack


# Checks whether a tree containts the differentiation variable or not.
# @param root: The root node of the binary tree.
# @param diff_var: The variable with respect to which the differentiation is performed.
# @return: True if the tree contains the differentiation variable, False otherwise
def has_diff_var(root, diff_var):
    q = deque([root])

    while q:
        node = q.popleft()

        if node.value == diff_var:
            return True

        if node.left:
            q.append(node.left)

        if node.right:
            q.append(node.right)

    return False
