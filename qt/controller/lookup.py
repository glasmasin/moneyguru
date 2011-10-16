# Created By: Virgil Dupras
# Created On: 2010-02-26
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QShortcut, QKeySequence

from ..ui.lookup_ui import Ui_Lookup

class Lookup(QWidget, Ui_Lookup):
    MODEL_CLASS = None
    
    def __init__(self, parent, model):
        QWidget.__init__(self, parent, Qt.Window)
        self.model = model
        self.model.view = self
        self._setupUi()
        
        self.searchEdit.searchChanged.connect(self.searchChanged)
        self.searchEdit.returnPressed.connect(self.returnPressed)
        self.namesList.currentRowChanged.connect(self.currentRowChanged)
        self.namesList.itemDoubleClicked.connect(self.itemDoubleClicked)
        self._shortcutUp.activated.connect(self.upPressed)
        self._shortcutDown.activated.connect(self.downPressed)
    
    def _setupUi(self):
        self.setupUi(self)
        self.searchEdit.immediate = True
        seq = QKeySequence(Qt.Key_Up)
        self._shortcutUp = QShortcut(seq, self, None, None, Qt.WidgetShortcut)
        seq = QKeySequence(Qt.Key_Down)
        self._shortcutDown = QShortcut(seq, self, None, None, Qt.WidgetShortcut)
    
    def _restoreSelection(self):
        self.namesList.setCurrentRow(self.model.selected_index)
    
    #--- Event Handlers
    def returnPressed(self):
        self.model.go()
    
    def searchChanged(self):
        self.model.search_query = str(self.searchEdit.text())
    
    def currentRowChanged(self, row):
        if row >= 0:
            self.model.selected_index = row
    
    def itemDoubleClicked(self, item):
        self.model.go()
    
    def upPressed(self):
        if self.namesList.currentRow() > 0:
            self.namesList.setCurrentRow(self.namesList.currentRow()-1)
    
    def downPressed(self):
        if self.namesList.currentRow() < self.namesList.count()-1:
            self.namesList.setCurrentRow(self.namesList.currentRow()+1)
    
    #--- model --> view
    def refresh(self):
        self.namesList.clear()
        self.namesList.addItems(self.model.names)
        self._restoreSelection()
        self.searchEdit.setText(self.model.search_query)
    
    def show(self):
        QWidget.show(self)
        self.searchEdit.setFocus()
        # see csv_options
        self.raise_()
    
    def hide(self):
        QWidget.hide(self)
    
