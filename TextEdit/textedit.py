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
			"&Open...", self, shortcut=QtGui.QKeySequence.Open,
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
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S,
			triggered=self.fileSaveAs)
		menu.addAction(self.actionSaveAs)
		menu.addSeparator()

		self.actionPrint = QtGui.QAction(
			QtGui.QIcon('document-print',
				QtGui.QIcon(rsrcPath + '/fileprint.png')),
			"&Print...", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtGui.QKeySequence.Print, triggered=self.filePrint)
		tb.addAction(self.actionPrint)
		menu.addAction(self.actionPrint)

		self.actionPrintPreview = QtGui.QAction(
			QtGui.QIcon.fromTheme('fileprint',
				QtGui.QIcon(rsrcPath + '/fileprint.png')),
			"Print Preview...", self,
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_P,
			triggered=self.filePrintPreview)
		menu.addAction(self.actionPrintPreview)

		self.actionPrintPdf = QtGui.QAction(
			QtGui.QIcon.fromTheme('exportpdf',
				QtGui.QIcon(rsrcPath + '/exportpdf.png')),
			"&Export PDF...", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_D,
			triggered=self.filePrintPdf)
		tb.addAction(self.actionPrintPdf)
		menu.addAction(self.actionPrintPdf)
		menu.addSeparator()

		self.actionQuit = QtGui.QAction("&Quit", self,
			shortcut=QtGui.QKeySequence.Quit, triggered=self.close)
		menu.addAction(self.actionQuit)


	def setupEditActions(self):
		tb = QtGui.QToolBar(self)
		tb.setWindowTitle("Edit Actions")
		self.addToolBar(tb)

		menu = QtGui.QMenu("&Edit", self)
		self.menuBar().addMenu(menu)

		self.actionUndo = QtGui.QAction(
			QtGui.QIcon.fromTheme('edit-undo',
				QtGui.QIcon(rsrcPath + '/editundo.png')),
			"&Undo", self, shortcut=QtGui.QKeySequence.Undo)
		tb.addAction(self.actionUndo)
		menu.addAction(self.actionUndo)

		self.actionRedo = QtGui.QAction(
			QtGui.QIcon.fromTheme('edit-redo',
				QtGui.QIcon(rsrcPath + '/editredo.png')),
			"&Redo", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtGui.QKeySequence.Redo)
		tb.addAction(self.actionRedo)
		menu.addAction(self.actionRedo)
		menu.addSeparator()

		self.actionCut = QtGui.QAction(
			QtGui.QIcon.fromTheme('edit-cut',
				QtGui.QIcon(rsrcPath + '/editcut.png')),
			"Cu&t", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtGui.QKeySequence.Cut)
		tb.addAction(self.actionCut)
		tb.addAction(self.actionCut)

		self.actionCopy = QtGui.QAction(
			QtGui.QIcon.fromTheme('edit-copy',
				QtGui.QIcon(rsrcPath + 'editcopy.png')),
			"&Copy", self, priority=QtGui.QIcon.LowPriority,
			shortcut=QtGui.QKeySequence.Copy)
		tb.addAction(self.actionCopy)
		menu.addAction(self.actionCopy)

		self.actionPaste = QtGui.QAction(
			QtGui.QIcon.fromTheme('edit-paste',
				QtGui.QIcon(rsrcPath + '/editpaste.png')),
			"&Paste", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtGui.QKeySequence.Paste,
			enabled=(len(QtGui.QAppcalition.clipboard().text()) != 0))
		tb.addAction(self.actionPaste)
		menu.addAction(self.actionPaste)

	def setupTextActions(self):
		tb = QtGui.QToolBar(self)
		tb.setWindowTitle("Format Actions")
		self.addToolBar(tb)

		menu = QtGui.QMenu("F&omat", self)
		self.menuBar().addMenu(menu)

		self.actionTextBold = QtGui.QAction(
			QtGui.QIcon.fromTheme('format-text-bold',
				QtGui.QIcon(rsrcPath + '/textbold.png')),
			"&Bold", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_B,
			triggered=self.textBold, checkable=True)
		bold = QtGui.QFont()
		bold.setBold(True)
		self.actionTextBold.setFont(bold)
		tb.addAction(self.actionTextBold)
		menu.addAction(self.actionTextBold)

		self.actionTextItalic = QtGui.QAction(
			QtGui.QIcon.fromTheme('format-text-italic',
				QtGui.QIcon(rsrcPath + '/textitalic.png')),
			"&Italic", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_I,
			triggered=self.textitalic, checkable=True)
		italic = QtGui.QFont()
		italic.setItalic(True)
		self.actionTextItalic.setFont(italic)
		tb.addAction(self.actionTextItalic)
		menu.addAction(self.actionTextItalic)

		self.actionTextUnderline = QtGui.QAction(
			QtGui.QIcon.fromTheme('format-text-underline',
				QtGui.QIcon(rsrcPath + '/textunder.png')),
			"&Underline", self, priority=QtGui.QAction.LowPriority,
			shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_U,
			triggered=self.textUnderline, checkable=True)
		underline = QtGui.Font()
		underline.setUnderline(True)
		self.actionTextUnderline.setFont(underline)
		tb.addAction(self.actionTextUnderline)
		menu.addAction(self.actionTextUnderline)

		menu.addSeparator()
		