from PySide6.QtWidgets import QApplication, QListWidget, QWidget, QVBoxLayout

class ListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ListApp")
        self.setLayout(self.center)
        self.layout = QVBoxLayout()
        self.listWidget = QListWidget()
        self.layout.addWidget(self.listWidget)


app = QApplication()
window = ListApp()
window.show()
app.exec_()

self.drugSearch = QCheckBox('Requires Drug Searches')
requirementsPageLayout.addWidget(self.drugSearch, 0, 0)

def licencee_data(self):
    self.data = [
        {'name': 'Alice', 'id': 236487, 'status': 'pending'},
        {'name': 'Bob', 'id': 232442, 'status': 'housed'},
        {'name': 'Will', 'id': 957120, 'status': 'exited'},
        {'name': 'Mike', 'id': 321757, 'status': 'pending'}
    ]


def licencee_searching(self):
    searchedItem = self.searchBar.text()
    if searchedItem == self.data[0]['name']: