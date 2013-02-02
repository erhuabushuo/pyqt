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

		helpMenu = QtGui.QMenu("Help", self)
		self.menuBar().addMenu(helpMenu)
		helpMenu.addAction("About", self.about)
		helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)

		self.textEdit = QtGui.QTextEdit(self)
		self.textEdit.currentCharFormatChanged.connect(
				self.currentCharFormatChanged)
		self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
		self.setCentralWidget(self.textEdit)
		self.textEdit.setFocus()
		self.setCurrentFileName()
		self.fontChanged(self.textEdit.font())
		self.colorChanged(self.textEdit.textColor())
		self.alignmentChanged(self.textEdit.alignment())
		self.textEdit.document().modificationChanged.connect(
				self.actionSave.setEnabled)
		self.textEdit.document().modificationChanged.connect(
				self.setWindowModifiled)
		self.textEdit.document().undoAvailable.connect(
				self.actionUndo.setEnabled)
		self.textEdit.document().redoAvailable.connect(
				self.actionRedo.setEnabled)
		self.setWindowModifiled(self.textEdit.document().isModified())
		self.actionSave.setEnabled(self.textEdit.document().isModified())
		self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
		self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())
		self.actionUndo.triggered.connect(self.textEdit.undo)
		self.actionRedo.triggered.connect(self.textEdit.redo)
		self.actionCut.setEnabled(False)
		self.actionCopy.setEnabled(False)
		self.actionCut.triggered.connect(self.textEdit.cut)
		self.actionPaste.triggered.connect(self.textEdit.copy)
		self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
		self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
		QtGui.QApplication.clipboard().dataChanged.connect(
				self.clipboardDataChanged)

		if fileName is None:
			fileName = ":/example.html"

		if not self.load(fileName):
			self.fileNew()

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
			enabled=(len(QtGui.QApplication.clipboard().text()) != 0))
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
		
		grp = QtGui.QActionGroup(self, triggered=self.textAlign)

		# Make sure the alignLeft is always left of the aligRight.
		if QtGui.QApplication.isLeftToRight():
			self.actionAlignLeft = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-left',
					QtGui.QIcon(rsrcPath + '/textleft.png')),
				"&Left", grp)
			self.actionAlignCenter = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-center',
					QtGui.QIcon(rsrcPath + '/textcenter.png')),
				"C&enter", grp)
			self.actionAlignRight = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-right',
					QtGui.QIcon(rsrcPath + '/textright.png')),
				"&Right", grp)
		else:
			self.actionAlignRight = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-right',
					QtGui.QIcon(rsrcPath + '/textright.png')),
				"&Right", grp)
			self.actionAlignCenter = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-center',
					QtGui.QIcon(rsrcPath + '/textcenter.png')),
				"C&enter", grp)
			self.actionAlignLeft = QtGui.QAction(
				QtGui.QIcon.fromTheme('format-justify-left',
					QtGui.QIcon(rsrcPath + '/textleft.png')),
				"&Left", grp)

		self.actionAlignJustify = QtGui.QAction(
			QtGui.QIcon.fromTheme('format-justify-fill',
				QtGui.QIcon(rsrcPath + '/textjusify.png')),
			"&Justify", grp)

		self.actionAlignLeft.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.QKey_L)
		self.actionAlignLeft.setCheckable(True)
		self.actionAlignLeft.setPrioprity(QtGui.QAction.LowPriority)

		self.actionAlignCenter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.QKey_E)
		self.actionAlignCenter.setCheckable(True)
		self.actionAlignCenter.setPrioprity(QtGui.QAction.LowPriority)

		self.actionAlignRight.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.QKey_R)
		self.actionAlignRight.setCheckable(True)
		self.actionAlignRight.setPrioprity(QtGui.QAction.LowPriority)

		self.actionAlignJustify.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.QKey_J)
		self.actionAlignJustify.setCheckable(True)
		self.actionAlignJustify.setPrioprity(QtGui.QAction.LowPriority)

		tb.addActions(grp.actions())
		menu.addActions(grp.actions())
		menu.addSeparator()

		pix = QtGui.QPixmap(16, 16)
		pix.fill(QtCore.Qt.black)
		self.actionTextColor = QtGui.QAction(QtGui.QIcon(pix), "&Color...",
				self, triggered=self.textColor)
		tb.addAction(self.actionTextColor)
		menu.addAction(self.actionTextColor)

		tb = QtGui.QToolBar(self)
		tb.setAllowedAreas(
				QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
		tb.setWindowTitle("Format Actions")
		self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
		self.addToolBar(tb)

		comboStyle = QtGui.QComboBox(tb)
		tb.addWidget(comboStyle)
		comboStyle.addItem("Standard")
		comboStyle.addItem("Bullet List (Disc)")
		comboStyle.addItem("Bullet List (Circle)")
		comboStyle.addItem("Bullet List (Square)")
		comboStyle.addItem("Bullet List (Decimal)")
		comboStyle.addItem("Bullet List (Alpha lower)")
		comboStyle.addItem("Bullet List (Alpha uppper)")
		comboStyle.addItem("Bullet List (Roman lower)")
		comboStyle.addItem("Bullet List (Roman uppper)")
		comboStyle.activated.connect(self.textStyle)

		self.comboFont = QtGui.QFontComboBox(tb)
		tbb.addWidget(self.comboFont)
		self.comboFont.activated[str].connect(self.textFamily)

		self.comboSize = QtGui.QComboBox(tb)
		self.comboSize.setObjectName("comboSize")
		tb.addWidget(self.comboSize)
		self.comboSize.setEditable(True)

		db = QtGui.QFontDatabase()
		for size in db.standradSizes():
			self.comboSize.addItem("%s" % (size))

		self.comboSize.activated[str].connect(self.textSize)
		self.comboSize.setCurrentIndex(
			self.comboSize.findText(
				"%s" % (QtGui.QApplication.font().pointSize())))


	def setCurrentFileName(self, fileName=''):
		self.fileName = fileName
		self.textEdit.document().setModified(False)

		if not fileName:
			shownName = 'untitled.txt'
		else:
			shownName = QtCore.QFileInfo(fileName).fileName()

		self.setWindowTitle("%s[*] - %s" % (shownName, "Rich Text"))
		self.setWindowModifiled(False)
