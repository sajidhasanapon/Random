import pandas as pd
from PyQt5 import QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.toolbar, 0, 0, 1, 4)
        self.layout.addWidget(self.canvas, 1, 0, 4, 4)
        self.layout.setColumnStretch(0, 4)
        self.layout.setColumnStretch(6, 0)

        self.filenameView = QLabel('Current file: ')
        self.layout.addWidget(self.filenameView, 1, 4, 1, 1)

        self.importDataButton = QPushButton('Import data')
        self.layout.addWidget(self.importDataButton, 2, 4, 1, 1)
        self.importDataButton.clicked.connect(self.importData)

        self.items = QListWidget()
        self.layout.addWidget(self.items, 3, 4, 1, 1)

        self.plotButton = QPushButton('Plot')
        self.layout.addWidget(self.plotButton, 4, 4, 1, 1)
        self.plotButton.clicked.connect(self.plot)

        self.data = None

    def importData(self):
        dlg = QFileDialog()
        selection = dlg.getOpenFileName(parent=self,
                                        caption="Select file",
                                        directory='./',
                                        filter="Comma Separated Values (*.csv)"
                                        )
        if selection[0] == '':
            return
        filename = selection[0]
        print(filename)
        self.data = pd.read_csv(filename)
        self.items.clear()
        for name in list(self.data.columns):
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsSelectable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.items.addItem(item)

        self.filenameView.setText(filename.split('/')[-1])
        self.fig.clear()
        self.canvas.draw()

        return

    def plot(self):
        columns = []
        for i in range(self.items.count()):
            item = self.items.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                columns.append(item.text())

        if len(columns) == 3:
            print(columns)
            x = self.data[columns[0]]
            y = self.data[columns[1]]
            z = self.data[columns[2]]
            ax = self.fig.add_subplot(111, projection='3d')
            ax.scatter3D(x, y, z, marker='o', color='blue')
            ax.set_xlabel(columns[0])
            ax.set_ylabel(columns[1])
            ax.set_zlabel(columns[2])

        elif len(columns) == 2:
            print(columns)
            x = self.data[columns[0]]
            y = self.data[columns[1]]
            ax = self.fig.add_subplot(111)
            ax.scatter(x, y, marker='o')
            ax.set_xlabel(columns[0])
            ax.set_ylabel(columns[1])

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Select 2/3 columns")
            msg.setWindowTitle("Oops!")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(lambda func: None)
            msg.exec()

        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = App()
    window.show()
    app.exec()
