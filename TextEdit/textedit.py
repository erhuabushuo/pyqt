#!/usr/bin/env python3
"""
	TextEdit
"""
import sys
from PyQt4 import QtCore, QtGui
import textedit_rc

if sys.platform.startswith('darwin'):
	rsrcPath = ":/images/mac"
else:
	rsrcPath = ":/images/win"

class TextEdit(QtGui.QMainWindow):
	def __init__(self, fileName=None, parent=None):
		super(TextEdit, self).__init__(parent)

		self.setWindowIcon(QtGui.QIcon(":/images/logo.png"))
		self.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
		self.setupFileActions()
		self.setupEditActions()
		self.setupTextActions()

	def setupFileActions(self):
		tb = QtGui.QToolBar(self)
		tb.setWindowTitle("File Actions")
		self.addToolBar(tb)

		menu = QtGui.QMenu("&File", self)
		self.menuBar().addMenu(menu)

		self.actionNew = QtGui.QAction(
			QtGui.QIcon.fromTheme('document-new',
				QtGui.QIcon(rsrcPath + '/filenew.png')),
			"&New", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtGui.QKeySequence.New, triggered=self.fileNew)
		tb.addAction(self.actionNew)
		menu.addAction(self.actionNew)

		self.actionOpen = QtGui.QAction(
			QtGui.QIon.fromTheme("document-open",
					QtGui.QIcon(rsrcPath + "/fileopen.png")),
			"&Open...", self, shotcut=QtGui.QKeySequence.Open,
			triggered=self.fileOpen)
		tb.addAction(self.actionOpen)
		menu.addAction(self.actionOpen)
		menu.addSeparator()

		self.actionSave = QtGui.QAction(
			QtGui.QIcon.fromTheme('document-save',
					QtGui.QIcon(rsrcPath + '/filesave.png')),
			"&Save", self, shortcut=QtGui.QKeySequence.Save,
			triggered=self.fileSave, enabled=False)
		tb.addAction(self.actionSave)
		menu.addAction(self.actionSave)

		self.actionSaveAs = QtGui.QAction("Save &As...", self,
			priority=QtGui.QAction.LowPriority,
			shotcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S,
			triggered=self.fileSaveAs)
		menu.addAction(self.actionSaveAs)
		menu.addSeparator()

		self.actionPrint = QtGui.QAction(
			QtGui.QIcon('document-print',
				QtGui.QIcon(rsrcPath + '/fileprint.png')),
			"&Print...", self, priority=QtGui.QAction.LowPriority,
			shotcut=QtGui.QKeySequence.Print, triggered=self.filePrint)
		tb.addAction(self.actionPrint)
		menu.addAction(self.actionPrint)

		self.actionPrintPreview = QtGui.QAction(
			QtGui.QIcon.fromTheme('fileprint',
				QtGui.QIcon(rsrcPath + '/fileprint.png')),
			"Print Preview...", self,
			shotcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_P,
			triggered=self.filePrintPreview)
		menu.addAction(self.actionPrintPreview)

		self.actionPrintPdf = QtGui.QAction(
			QtGui.QIcon.fromTheme('exportpdf',
				QtGui.QIcon(rsrcPath + '/exportpdf.png')),
			"&Export PDF...", self, priority=QtGui.QAction.LowPriority,
			shotcut=QtCore.Qt.CTRL + QtCore.Qt.Key_D,
			triggered=self.filePrintPdf)
		tb.addAction(self.actionPrintPdf)
		menu.addAction(self.actionPrintPdf)
		menu.addSeparator()

		self.actionQuit = QtGui.QAction("&Quit", self,
			shotcut=QtGui.QKeySequence.Quit, triggered=self.close)
		menu.addAction(self.actionQuit)

		