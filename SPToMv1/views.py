# -*- coding: utf-8 -*-

##############################################
#
# Created by : Tristan Le Granché
# Contact : tristan.legranche@gmail.com
# GitHub repository : https://github.com/Strangenoise/SubstancePainterToMaya
# Last edit made the : 11/13/2019
#
# LICENCE GNU GPL 3
#
# This file is part of SubstancePainterToMaya.
#
# SubstancePainterToMaya is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# SubstancePainterToMaya is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see https://www.gnu.org/licenses/.
#
##############################################

# Libraries
from PySide2 import QtWidgets, QtCore, QtGui


class ListView(QtWidgets.QListWidget):
    leftClicked = QtCore.Signal(str)
    middleClicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):

        super(ListView, self).__init__(parent)

        self.parent = parent
        self.position = None
        self.basePalette = self.palette()
        self.keyPalette = self.palette()
        self.keyPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(192, 32, 32))
        self.resetPalette = self.palette()
        self.resetPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(32, 128, 192))

    def mousePressEvent(self, event):

        if event.buttons() & QtCore.Qt.MiddleButton:
            self.middleClicked.emit(self.indexAt(event.pos()))
            return

        elif event.buttons() & QtCore.Qt.RightButton:
            return

        elif event.buttons() & QtCore.Qt.LeftButton:
            self.leftClicked.emit('Click')
            QtWidgets.QListView.mousePressEvent(self, event)
            return

    def initial_blink(self, mode):

        self.setPalette(self.keyPalette if mode == "key" else self.resetPalette)
        self.repaint()

    def blink(self):

        QtCore.QTimer.singleShot(200, self.un_blink)

    def un_blink(self):

        self.setPalette(self.basePalette)

class textureItem(object):
    def __init__(self, name="", isSubObject=False):
        self.name = name
        self.isSubObject = isSubObject


class textureModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(textureModel, self).__init__(parent)

        self.items_list = []
        self.italic = QtGui.QFont()
        self.italic.setItalic(1)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items_list)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def data(self, index, role):
        if index.isValid():
            item = self.items_list[index.row()]
            if role == QtCore.Qt.DisplayRole:
                return item.name
            elif role == QtCore.Qt.FontRole:
                if item.isSubObject:
                    return self.italic
            elif role == QtCore.Qt.UserRole:
                return item.name
            elif role == QtCore.Qt.UserRole + 1:
                return ("1" if item.isSubObject else "0") + item.name

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):

        self.beginInsertRows(parent, row, row + count - 1)
        # items already added with appendItems(), but sometimes crash when insertRows() is not explicitly called...
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):

        self.beginRemoveRows(parent, row, row + count - 1)
        del (self.items_list[row:row + count])
        self.endRemoveRows()
        return True

    def appendItems(self, items):
        self.items_list.extend(items)
        self.insertRows(self.rowCount(), len(items))

    def deleteItems(self, names):

        indices = [i for i, item in enumerate(self.items_list) if item.name in names]
        for i in reversed(sorted(indices)):
            self.removeRows(i, 1)

    def load(self, items_list):

        del (self.items_list[:])
        self.items_list.extend(items_list)
        self.endResetModel()

    def clear(self):

        del (self.items_list[:])
        self.endResetModel()

class TreeNode(object):

    def __init__(self, row, parent):
        self.row = row
        self.parent = parent
        self.children = []