#!/usr/bin/python

try:
    import tkinter as tk
except:
    import Tkinter as tk

from operator import add as OpAdd
from math import floor
import time
import random

from GameOfLife import GameOfLife
import colourutils
from cellfile import GetCellsFromFile

fileCellpath = 'cells.ini'

colourTypeMessages = ('Background', 'Foreground')


def ColourTypeToString(isForegound):
    return colourTypeMessages[isForegound]


def ColourTypeToChangeString(isForeground):
    return 'Change %s' % ColourTypeToString(isForeground)


# green on black
DEFAULT_FOREGROUND_COLOUR = 0x00ff00
DEFAULT_BACKGROUND_COLOUR = 0x000000

goingStringEnum = ('Go', 'Stop')


def GoingToString(isGoing):
    return goingStringEnum[isGoing]


def BoolToPlusMinusOne(inputBool):
    return (bool(inputBool) * 2) - 1


_MINIMUM_SIDE = 1


class GUI(tk.Tk):
    """A custom graphical user interface for the GameOfLife Class

    First working Iteration() at 10:08Pm 2nd July 2008"""

    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.title('Game Of Life')

        self.grid()

        # leave at defaults for a 2 dimensional game of life with John Conway standard rules (3/23)
        self.GOL = GameOfLife()

        self.CreateWidgets()
        self.Bindings()
        self.Reset()
        self.ResetColour()

    def Reset(self):
        self.ChangeGoNow(False)
        self.side = 5
        self.GAP = 1
        self.InvertZoom = False
        self.ZoomIncrement = 1

        self.GOL.Reset()
        self.ResetOriginClick()
        self.Display()
        self.DisplayGoingToString()

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, side):
        self._side = max(int(side), _MINIMUM_SIDE)

    def ResetColour(self):
        self.ChangeForeground(DEFAULT_FOREGROUND_COLOUR)
        self.ChangeBackground(DEFAULT_BACKGROUND_COLOUR)

    def Key(self, event):
        if event.keysym in self.keyDict:
            self.keyDict[event.keysym]()

    def CloseProgram(self):
        self.ChangeGoNow(False)
        self.destroy()

    def CreateWidgets(self):
        self.vGoStop = tk.StringVar()

        fCont = tk.Frame(self)
        tk.Button(fCont, text='Reset', command=self.Reset).pack(side=tk.LEFT)
        tk.Button(fCont, text='Iterate', command=self.Iterate).pack(side=tk.LEFT)
        tk.Button(fCont, textvariable=self.vGoStop, command=self.GoStop).pack(side=tk.LEFT)
        tk.Button(fCont, text='Reset Colour', command=self.ResetColour).pack(side=tk.LEFT)
        tk.Button(fCont, text=ColourTypeToChangeString(True), command=self.ChangeForeground).pack(side=tk.LEFT)
        tk.Button(fCont, text=ColourTypeToChangeString(False), command=self.ChangeBackground).pack(side=tk.LEFT)
        tk.Button(fCont, text='Load Cells', command=self.LoadCells).pack(side=tk.LEFT)
        fCont.grid(sticky=tk.W)

        self.cnvs = tk.Canvas(bd=0)  # put canvas in same GUI rather than #master = Tk() (new one)
        self.cnvs.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

    def Bindings(self):
        self.protocol('WM_DELETE_WINDOW', self.CloseProgram)

        self.keyDict = {
            'Escape': self.CloseProgram,
            'Delete': self.Reset,
            'r': self.Reset,
            'Return': self.Iterate,
            'i': self.Iterate,
            'g': self.Go,
            's': self.Stop,
            'space': self.GoStop,
            'f': self.ChangeForeground,
            'b': self.ChangeBackground,
            'l': self.LoadCells,
            # 'Left': '',
            # 'Right': '',
            # 'Up': '',
            # 'Down': '',
        }
        self.bind('<Key>', self.Key)
        self.cnvs.bind('<Button-1>', self.PlacePointClick)  # left mouse click
        self.cnvs.bind('<B1-Motion>', self.PlacePointDrag)
        self.cnvs.bind('<Button-2>', self.ResetOriginClick)  # right mouse click
        self.cnvs.bind('<Button-3>', self.ChangeOriginClick)
        self.cnvs.bind('<B3-Motion>', self.ChangeOriginDrag)
        self.bind('<MouseWheel>', self.MouseWheelZoom)  # mouse wheel
        self.bind('<Button-4>', self.MouseWheelZoom)
        self.bind('<Button-5>', self.MouseWheelZoom)

        self.cnvs.bind('<Configure>', self.CanvasResize)

    def PointDimToCellDim(self, i):
        return int(i // (self.side + self.GAP))

    def PointToCell(self, *point):
        '''Internal method to Convert a Point on the canvas to a Tuple refering to the Cell it is in.
        '''
        canvasedPoints = self.cnvs.canvasx(point[0]), self.cnvs.canvasy(point[1])
        return tuple(map(self.PointDimToCellDim, canvasedPoints))

    def PlacePointClick(self, event):
        # Using normal variable rather than object one stops doubling up of turning on and off or vice versa of a single point (re-entrancy).
        pointPlace = self.PointToCell(event.x, event.y)

        self.GOL.ToggleCell(pointPlace)

        self.pointPlace = pointPlace
        # store the value so all those in any directly subsequent PlacePointDrag will use it
        self.pointPlaceValue = self.GOL.IsCellAlive(pointPlace)
        self.Display()

    def PlacePointDrag(self, event):
        '''Assumes that PlacePointClick sets self.point otherwise in setup it must be set to "= None".
        '''
        pointPlace = self.PointToCell(event.x, event.y)
        if not pointPlace == self.pointPlace:
            # remove final argument to replace the value of all cells rather than keep value
            self.GOL.SetCell(pointPlace, self.pointPlaceValue)
            self.pointPlace = pointPlace
            self.Display()

    def ResetOriginClick(self, event=None):
        '''Default scroll to 0,0 in top left.
        '''
        self.cnvs.config(scrollregion='0 0 %s %s' % (self.cnvs.cget('width'), self.cnvs.cget('height')))

    def ChangeOriginClick(self, event):
        self.pointScroll = self.cnvs.canvasx(event.x), self.cnvs.canvasy(event.y)

    def ChangeOriginDrag(self, event):
        # for the first two remove float part and convert to integer
        curScroll = (floor(float(value)) for value in self.cnvs.cget('scrollregion').split()[:2])
        toScroll = self.pointScroll[0] - self.cnvs.canvasx(event.x), self.pointScroll[1] - self.cnvs.canvasy(event.y)
        goingScroll = tuple(map(OpAdd, curScroll, toScroll))

        self.cnvs.config(scrollregion='{} {} {} {}'.format(
            goingScroll[0],
            goingScroll[1],
            goingScroll[0] + int(self.cnvs.cget('width')),
            goingScroll[1] + int(self.cnvs.cget('height'))
        ))

        self.pointScroll = self.cnvs.canvasx(event.x), self.cnvs.canvasy(event.y)

    def ZoomStep(self):
        return BoolToPlusMinusOne(not self.InvertZoom) * self.ZoomIncrement

    def MouseWheelZoom(self, event):
        '''Respond to Linux (event.num) or Windows (event.delta) wheel events.
        Zooms in and out.
        Focused on (0,0) i.e the original top left corner place.
        '''
        _DELTA = 120
        zoomStep = self.ZoomStep()

        if event.num == 4 or event.delta == _DELTA:
            # mouse wheel up
            self.side += zoomStep
        elif event.num == 5 or event.delta == -_DELTA:
            # mouse wheel down
            self.side -= zoomStep

        self.Display()

    def CellToPoint(self, end, *cell):
        return tuple([coordinate * (self.side + self.GAP) + (end * self.side) for coordinate in cell])

    def PlaceCellOnCanvas(self, cell):
        self.cnvs.create_rectangle(self.CellToPoint(False, *cell), self.CellToPoint(True, *cell), fill=self.foregroundTKColour, width=0)

    def Display(self):
        '''Deletes any relevant contents of the canvas called "cnvs" replacing them with an updated view of the cells.
        the canvas is always double-buffered. Just create or modify
        canvas items as usual. When Tk returns to the event loop,
        the canvas is redrawn as soon as possible.
        http://mail.python.org/pipermail/python-list/2001-March/073778.html
        '''
        self.cnvs.delete(tk.ALL)
        list(map(self.PlaceCellOnCanvas, self.GOL()))

    def Iterate(self):
        self.ChangeGoNow(False)
        self.GOL.Iterate()
        self.Display()

    def Go(self):
        if not self.goNow:
            self.GoStop()

    def Stop(self):
        if self.goNow:
            self.GoStop()

    def GoStop(self):
        '''Must be implemented as a separate thread or check GUI for events at set intervals otherwise locks up.
        '''
        self.ChangeGoNow()
        while self.goNow:
            self.GOL.Iterate()
            self.Display()
            self.cnvs.update()
            # time.sleep(.1)

    def DisplayGoingToString(self):
        self.vGoStop.set(GoingToString(self.goNow))

    def ChangeGoNow(self, newValue=None):
        if newValue is None:
            self.goNow = not self.goNow
        else:
            self.goNow = bool(newValue)

        self.DisplayGoingToString()

    def RandomIfUnspecifiedColour(self, colour=None):
        if colour is None:
            colour = colourutils.RandomColour()
        return colour

    def PrintColour(self, colour, isForeground):
        print('%s Colour Changed To: %s' % (ColourTypeToString(isForeground), colourutils.StandardHexColourPadded(colour)))

    def ChangeForeground(self, colour=None):
        '''If Foreground colour is unspecified a random one will be chosen.
        '''
        colour = self.RandomIfUnspecifiedColour(colour)
        tkColour = colourutils.TKHexColourPadded(colour)

        self.PrintColour(colour, isForeground=True)
        self.cnvs.itemconfig(tk.ALL, fill=tkColour)

        # storing choices
        self.foreground = colour
        self.foregroundTKColour = tkColour

    def ChangeBackground(self, colour=None):
        '''If Background colour is unspecified a random one will be chosen.
        '''
        colour = self.RandomIfUnspecifiedColour(colour)
        tkColour = colourutils.TKHexColourPadded(colour)

        self.PrintColour(colour, isForeground=False)
        self.cnvs.config(bg=tkColour)

        # storing choices
        self.background = colour
        self.backgroundTKColour = tkColour

    def ClearPlaceGlider(self):
        self.Reset()
        self.GOL.Glider()
        self.Display()

    def LoadCells(self):
        try:
            cells = GetCellsFromFile(fileCellpath)
        except IOError:
            print('File "%s" not found.' % fileCellpath)
        else:
            self.GOL.cells = cells
            self.Display()

    def CanvasResize(self, event):
        '''Change the size stored in the canvas when the window is resized so ChangeOriginDrag works properly.
        '''
        self.cnvs['width'], self.cnvs['height'] = event.width-4, event.height-4


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
