# union_find.py
def find(cell):
    """Find with path compression (explicit path tracking)"""
    path = []
    current = cell
    while current.parent != current:
        path.append(current)
        current = current.parent
    root = current
    # Path compression
    for node in path:
        node.parent = root
    return root


def union(cell1, cell2):
    """Union by rank"""
    root1 = find(cell1)
    root2 = find(cell2)

    if root1 == root2:
        return

    if root1.rank <= root2.rank:
        root1.parent = root2
        root2.rank += root1.rank
    elif root1.rank > root2.rank:
        root2.parent = root1
        root1.rank += root2.rank
    
