import sys, time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar

import numpy as np
import pylab as pl

import random



#-----The class that contains a central widget, the menu and toolbar-----
class Window(QMainWindow):
    
    def __init__(self, parent=None):

        super(Window, self).__init__(parent)

        Window.data = 'initialization'  
        
        self.UI()

    def UI(self):
                    
        self.central_widget = VisualizeWidget(self)
        self.setCentralWidget(self.central_widget)

        #----------Window's parameters (Size, Title, Icon)---------------
        #self.setGeometry(100, 100, 800, 500)
        self.showMaximized()
        self.setWindowTitle('Particle Tracking Velocimetry')
        self.setWindowIcon(QIcon('tuc_logo.png'))
        #----------------------------------------------------------------


        #----------------Creation of Menu's Actions----------------------
        openFile_menu = QAction(QIcon('open_logo.png'), 'Open...', self)
        #openFile_menu.setShortcut('Ctrl+O')
        openFile_menu.setStatusTip('Open new File')
        openFile_menu.triggered.connect(self.showDialog)
        
        exitAction_menu = QAction(QIcon('exit_logo.png'), '&Exit', self)        
        exitAction_menu.setShortcut('Ctrl+E')
        exitAction_menu.setStatusTip('Exit application')
        exitAction_menu.triggered.connect(self.close_application)

        helpAction_menu = QAction('About Fasmatech', self)
        helpAction_menu.triggered.connect(self.about_fasmatech)
        #----------------------------------------------------------------


        #--------------Creation of Toolbar's Actions---------------------
        openFile_toolbar = QAction(QIcon('open_logo.png'), 'Open...', self)
        openFile_toolbar.setShortcut('Ctrl+O')
        openFile_toolbar.setStatusTip('Open new File')
        openFile_toolbar.triggered.connect(self.showDialog)
        #----------------------------------------------------------------

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile_menu)
        fileMenu.addAction(exitAction_menu)
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(helpAction_menu)

        self.toolbar = self.addToolBar('Open...')
        self.toolbar.addAction(openFile_toolbar)
        
        
    #------Creates a pop up window when "About Fasmatech" is clicked-----
    def about_fasmatech(self):
        print("Opening a new popup window...")
        self.dialog = MyPopupDialog()
        #self.dialog.setGeometry(QRect(100, 100, 300, 500))
        self.dialog.show()
    #--------------------------------------------------------------------
        

    #----------Displays a Browser window to choose .txt files------------
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', 'TXT File (*.txt)') #QFileDialog which is used to select a file.

        if fname[0]:    #The selected file name is readand the contents of the file are set to the text edit widget.
            Window.data = np.loadtxt(fname[0])
    #--------------------------------------------------------------------
        

    #---Asks whether to terminate the appplication when Exit is clicked--
    def close_application(self):
        choice = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:            
            print("The application was terminated.")
            sys.exit()
        else:
            pass
    #--------------------------------------------------------------------
        
        
    #--Asks whether to terminate the appplication when the"x" is clicked-
    def closeEvent(self, event):

        choice = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print("The application was terminated.")
            event.accept()            
        else:
            event.ignore()
#------------------------------------------------------------------------





#-----The class that contains all the Widgets for the popup window-------
class MyPopupDialog(QWidget):
    def __init__(self, parent=None):
        super(MyPopupDialog, self).__init__(parent)

        self.setGeometry(QRect(100, 100, 300, 350))    #All three methods have been inherited from the QWidget class.
        self.setWindowTitle('About Fasmatech')
        self.setWindowIcon(QIcon('fasmatech_picture.png'))

        label1 = QLabel('Fasmatech')
        label1.setFont(QFont('SansSerif', 20))
        label1.setAlignment(Qt.AlignCenter)

        centralImage = QPixmap("fasmatech_picture.png")
        label2 = QLabel(self)
        label2.setPixmap(centralImage)
        label2.setAlignment(Qt.AlignCenter)

        label3 = QLabel('\n \n Fasmatech is a high technology company,\n focused on mass spectrometry and ion \nmobility instrumentation R&D services,\n custom devices design and \nmanufacturing, ion analysis peripheral \ntechnologies and their applications. \n\n ---------------------------------------- \n\n Email: info@fasmatech.com \n \n http://fasmatech.com')
        label3.setFont(QFont('SansSerif', 10))
        label3.setAlignment(Qt.AlignCenter)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(label1)
        self.mainLayout.addWidget(label2)
        self.mainLayout.addWidget(label3)

        self.setLayout(self.mainLayout)
#------------------------------------------------------------------------




#--The class that contains all the Widgets and imported into QMainWindow-
class VisualizeWidget(QWidget):

    def __init__(self, parent):
        super(VisualizeWidget, self).__init__(parent)


        #----Create the left layout that contains the folder treeview.---
        self.folderLayout = QWidget();

        self.pathRoot = QDir.rootPath()
        
        self.dirmodel = QFileSystemModel(self)
        self.dirmodel.setRootPath(QDir.currentPath())
        #self.dirmodel.setRootPath(QDir.rootPath())
        #self.dirmodel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)    # Don't show files, just folders

        self.indexRoot = self.dirmodel.index(self.dirmodel.rootPath())


        self.folder_view = QTreeView();
        self.folder_view.setModel(self.dirmodel)
        self.folder_view.setRootIndex(self.indexRoot)
        self.folder_view.clicked.connect(self.FolderViewClicked)


        self.selectionModel = self.folder_view.selectionModel()
        
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.folder_view)
        
        self.folderLayout.setLayout(self.left_layout)
        #----------------------------------------------------------------

        
        #-------Create the right layout that contains the plot canvas.---    
        self.plotLayout = QWidget();

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        self.color = plt.cm.jet    #The initial colormap is "jet"

        #Create a ComboBox that contains the colormaps
        self.combo = QComboBox(self)
        self.combo.addItem("Jet")
        self.combo.addItem("Spectral")
        self.combo.addItem("Autumn")
        self.combo.addItem("Cool")
        self.combo.addItem("Copper")
        self.combo.addItem("Winter")

        self.combo.activated[str].connect(self.onActivated)

        self.comboLayout = QHBoxLayout()
        self.comboLayout.addWidget(self.button)
        self.comboLayout.addWidget(self.combo)
        

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.toolbar)
        self.right_layout.addWidget(self.canvas)
        self.right_layout.addLayout(self.comboLayout)

        self.plotLayout.setLayout(self.right_layout)
        #----------------------------------------------------------------

        #Use of a QSplitter to split the folderView with the canvas
        splitter_filebrowser = QSplitter(Qt.Horizontal)
        splitter_filebrowser.addWidget(self.folderLayout)
        splitter_filebrowser.addWidget(self.plotLayout)
        splitter_filebrowser.setStretchFactor(1, 1)

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter_filebrowser)
  
        self.setLayout(hbox)


    #----------------When ComboBox's choice is changed------------------
    def onActivated(self, text):

        if self.combo.currentText() == "Jet":
            self.color = plt.cm.jet
        elif self.combo.currentText() == "Spectral":
            self.color = plt.cm.spectral
        elif self.combo.currentText() == "Autumn":
            self.color = plt.cm.autumn
        elif self.combo.currentText() == "Cool":
            self.color = plt.cm.cool
        elif self.combo.currentText() == "Copper":
            self.color = plt.cm.copper
        elif self.combo.currentText() == "Winter":
            self.color = plt.cm.winter
    #--------------------------------------------------------------------

           
        
    #-------Creation of the plot when "plot" buttons is clicked----------
    def plot(self, color):

        if Window.data == "initialization":    #If no file is imported
            pass    #Do nothing
        else:

            x = Window.data[:,0]    #The x coordinate
            y = Window.data[:,1]    #The y coordinate
            
            vx = Window.data[:,2]   #The axial (Vx) velocity
            vy = Window.data[:,3]    #The radial (Vy) velocity


            v = Window.data[:,4]    #The (V) velocity

            #Instead of ax.hold(False)
            self.figure.clear()

            #Create an axis
            ax = self.figure.add_subplot(111)

            colormap = self.color

            #Plot the data
            q = plt.quiver(x, y, vx, vy, v, cmap = colormap, linewidth=0.01, width=0.002, headwidth=3)
            cb = plt.colorbar(q)

            ax.set_title("Axial Velocity")
            ax.set_xlabel('x (mm)')
            ax.set_ylabel('y (mm)')

##            ax.set_xlim([-1, 2000])
##            ax.set_ylim([-1, 2000])
            grd = plt.grid(True)

           
            #Refresh canvas
            self.canvas.draw()
    #--------------------------------------------------------------------



    #If the folderView is clicked:
    @pyqtSlot(QModelIndex)    
    def FolderViewClicked(self, index):
        indexItem = self.dirmodel.index(index.row(), 0, index.parent())    #Expand the folders

        fileName = self.dirmodel.fileName(indexItem)
        #print(fileName)

        fileType = self.dirmodel.type(indexItem)
        #print(fileType)
  

        with open(fileName) as f:
            if fileType == "txt File":  #Check that only .txt files are imported
                Window.data = np.loadtxt(fileName)     
            
            else:
                pass
#-----------------------------------------------------------------------




#-------------Creation of the SplashScreen (video)----------------------
class MovieSplashScreen(QSplashScreen):
        def __init__(self, movie, parent = None):
            
            movie.jumpToFrame(0)
            pixmap = QPixmap(movie.frameRect().size())
           
            QSplashScreen.__init__(self, pixmap)
            self.movie = movie
            self.movie.frameChanged.connect(self.repaint)
       
        def showEvent(self, event):
            self.movie.start()
               
        def hideEvent(self, event):
            self.movie.stop()
               
        def paintEvent(self, event):
       
            painter = QPainter(self)
            pixmap = self.movie.currentPixmap()
            self.setMask(pixmap.mask())
            painter.drawPixmap(0, 0, pixmap)
               
        def sizeHint(self):
               
            return self.movie.scaledSize()
      

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    movie = QMovie("gif (5).gif")
    splash = MovieSplashScreen(movie)
    splash.show()
	
    start = time.time()
       
    while movie.state() == QMovie.Running and time.time() < start+7:
        app.processEvents()

    win = Window()
    win.show()
    splash.finish(win)
    app.exec_()
#-----------------------------------------------------------------------




#------------Creation of the SplashScreen (picture)---------------------

##if __name__ == '__main__':
##    import sys, time
##    
##    app = QApplication(sys.argv)
##
##    splash_pix = QPixmap('a.jpg')
##    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
##    splash.setMask(splash_pix.mask())
##    splash.show()
##    app.processEvents()
##
##    time.sleep(2)
##
##
##    win = Window()
##    win.show()
##    splash.finish(win)
##    app.exec_()
    

