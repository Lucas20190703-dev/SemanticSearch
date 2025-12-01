class TreeItem:
    def __init__(self, name, path = "", parent=None):
        self.name = name
        self.path = path if path else name
        self.parent = parent
        self.children = []
    
    def childCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]

    def addChild(self, item):
        self.children.append(item)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
