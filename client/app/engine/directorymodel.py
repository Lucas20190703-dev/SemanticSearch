import requests
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel
from app.engine.treeitem import TreeItem

class DirectoryModel(QAbstractItemModel):
    def __init__(self, api_url, parent=None):
        super().__init__(parent)
        self.rootItem = TreeItem("Root")
        self.loadData(api_url)

    def loadData(self, url):
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()  # raises HTTPError for non-200
            data = res.json()       # may raise ValueError if invalid JSON
            self._populate(self.rootItem, data)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError as e:
            print(f"Invalid JSON: {e}")        

    def _populate(self, parent: TreeItem, nodes):
        for node in nodes:
            # path = f"{parent.path}/{node['name']}" if parent != self.rootItem else node["name"]
            item = TreeItem(node["name"], node["path"], parent)
            parent.addChild(item)
            self._populate(item, node.get("children", []))

    def rowCount(self, parent):
        item = parent.internalPointer() if parent.isValid() else self.rootItem
        return item.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
        if role == Qt.DisplayRole or role == Qt.UserRole + 1:
            return item.name
        if role == Qt.UserRole + 2:
            return item.path
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        childItem = parentItem.child(row)
        return self.createIndex(row, column, childItem)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent
        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def roleNames(self):
        roles = super().roleNames()
        roles[Qt.UserRole + 1] = b'display'
        roles[Qt.UserRole + 2] = b'path'
        return roles
 
