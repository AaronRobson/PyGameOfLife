import tkinter as tk

from operator import add
from math import floor
# import time

from gameoflife import GameOfLife
import colourutils
from cellfile import get_cells_from_file

file_cell_path = 'cells.ini'

colour_type_messages = ('Background', 'Foreground')


def colour_type_to_string(is_foregound):
    return colour_type_messages[is_foregound]


def colour_type_to_change_string(is_foreground):
    return 'Change %s' % colour_type_to_string(is_foreground)


# green on black
default_foreground_colour = 0x00ff00
default_background_colour = 0x000000

going_string_enum = ('Go', 'Stop')


def going_to_string(is_going):
    return going_string_enum[is_going]


def bool_to_plus_minus_one(input_bool):
    return (bool(input_bool) * 2) - 1


minimum_size = 1


class Gui(tk.Tk):
    """A custom graphical user interface for the GameOfLife Class

    First working Iteration() at 10:08Pm 2nd July 2008"""

    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.title('Game Of Life')

        self.grid()

        # leave at defaults for a 2 dimensional game of life with
        # John Conway standard rules (3/23)
        self.gol = GameOfLife()

        self.create_widgets()
        self.bindings()
        self.reset()
        self.reset_colour()

    def reset(self):
        self.change_go_now(False)
        self.side = 5
        self.gap = 1
        self.invert_zoom = False
        self.zoom_increment = 1

        self.gol.reset()
        self.reset_origin_click()
        self.display()
        self.display_going_to_string()

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, side):
        self._side = max(int(side), minimum_size)

    def reset_colour(self):
        self.change_foreground(default_foreground_colour)
        self.change_background(default_background_colour)

    def key(self, event):
        if event.keysym in self.key_dict:
            self.key_dict[event.keysym]()

    def close_program(self):
        self.change_go_now(False)
        self.destroy()

    def create_widgets(self):
        self.v_go_stop = tk.StringVar()

        f_cont = tk.Frame(self)
        tk.Button(
            f_cont,
            text='Reset',
            command=self.reset).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            text='Iterate',
            command=self.iterate).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            textvariable=self.v_go_stop,
            command=self.go_stop).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            text='Reset Colour',
            command=self.reset_colour).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            text=colour_type_to_change_string(True),
            command=self.change_foreground).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            text=colour_type_to_change_string(False),
            command=self.change_background).pack(side=tk.LEFT)
        tk.Button(
            f_cont,
            text='Load Cells',
            command=self.load_cells).pack(side=tk.LEFT)
        f_cont.grid(sticky=tk.W)

        # put canvas in same GUI rather than #master = Tk() (new one)
        self.cnvs = tk.Canvas(bd=0)
        self.cnvs.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

    def bindings(self):
        self.protocol('WM_DELETE_WINDOW', self.close_program)

        self.key_dict = {
            'Escape': self.close_program,
            'Delete': self.reset,
            'r': self.reset,
            'Return': self.iterate,
            'i': self.iterate,
            'g': self.go,
            's': self.stop,
            'space': self.go_stop,
            'f': self.change_foreground,
            'b': self.change_background,
            'l': self.load_cells,
            # 'Left': '',
            # 'Right': '',
            # 'Up': '',
            # 'Down': '',
        }
        self.bind('<Key>', self.key)
        self.cnvs.bind('<Button-1>', self.place_point_click)  # left mouse
        self.cnvs.bind('<B1-Motion>', self.place_point_drag)
        self.cnvs.bind('<Button-2>', self.reset_origin_click)  # right mouse
        self.cnvs.bind('<Button-3>', self.change_origin_click)
        self.cnvs.bind('<B3-Motion>', self.change_origin_drag)
        self.bind('<MouseWheel>', self.mouse_wheel_zoom)  # mouse wheel
        self.bind('<Button-4>', self.mouse_wheel_zoom)
        self.bind('<Button-5>', self.mouse_wheel_zoom)

        self.cnvs.bind('<Configure>', self.canvas_resize)

    def point_dim_to_cell_dim(self, i):
        return int(i // (self.side + self.gap))

    def point_to_cell(self, *point):
        '''Internal method to Convert a Point on the canvas to
        a Tuple refering to the Cell it is in.
        '''
        canvased_points = (
            self.cnvs.canvasx(point[0]),
            self.cnvs.canvasy(point[1]))
        return tuple(map(self.point_dim_to_cell_dim, canvased_points))

    def place_point_click(self, event):
        '''Using normal variable rather than object one stops doubling up
        of turning on and off or vice versa of a single point (re-entrancy).
        '''
        point_place = self.point_to_cell(event.x, event.y)

        self.gol.toggle_cell(point_place)

        self.point_place = point_place
        # store the value so all those in any directly subsequent
        # place_point_drag will use it
        self.point_place_value = self.gol.is_cell_alive(point_place)
        self.display()

    def place_point_drag(self, event):
        '''Assumes that PlacePointClick sets self.point otherwise
        in setup it must be set to "= None".
        '''
        point_place = self.point_to_cell(event.x, event.y)
        if not point_place == self.point_place:
            # remove final argument to replace the value of all cells
            # rather than keep value
            self.gol.set_cell(point_place, self.point_place_value)
            self.point_place = point_place
            self.display()

    def reset_origin_click(self, event=None):
        '''Default scroll to 0,0 in top left.
        '''
        self.cnvs.config(scrollregion='0 0 %s %s' % (
            self.cnvs.cget('width'),
            self.cnvs.cget('height')))

    def change_origin_click(self, event):
        self.point_scroll = (
            self.cnvs.canvasx(event.x),
            self.cnvs.canvasy(event.y))

    def change_origin_drag(self, event):
        # for the first two remove float part and convert to integer
        cur_scroll = (
            floor(float(value))
            for value in self.cnvs.cget('scrollregion').split()[:2])
        to_scroll = (
            self.point_scroll[0] - self.cnvs.canvasx(event.x),
            self.point_scroll[1] - self.cnvs.canvasy(event.y))
        going_scroll = tuple(map(add, cur_scroll, to_scroll))

        self.cnvs.config(scrollregion='{} {} {} {}'.format(
            going_scroll[0],
            going_scroll[1],
            going_scroll[0] + int(self.cnvs.cget('width')),
            going_scroll[1] + int(self.cnvs.cget('height'))
        ))

        self.point_scroll = (
            self.cnvs.canvasx(event.x),
            self.cnvs.canvasy(event.y))

    def zoom_step(self):
        return bool_to_plus_minus_one(not self.invert_zoom) * \
            self.zoom_increment

    def mouse_wheel_zoom(self, event):
        '''Respond to Linux (event.num) or Windows (event.delta) wheel events.
        Zooms in and out.
        Focused on (0,0) i.e the original top left corner place.
        '''
        delta = 120
        zoom_step = self.zoom_step()

        if event.num == 4 or event.delta == delta:
            # mouse wheel up
            self.side += zoom_step
        elif event.num == 5 or event.delta == -delta:
            # mouse wheel down
            self.side -= zoom_step

        self.display()

    def cell_to_point(self, end, *cell):
        return tuple([
            coordinate * (self.side + self.gap) + (end * self.side)
            for coordinate in cell])

    def place_cell_on_canvas(self, cell):
        self.cnvs.create_rectangle(
            self.cell_to_point(False, *cell),
            self.cell_to_point(True, *cell),
            fill=self.foreground_tk_colour, width=0)

    def display(self):
        '''Deletes any relevant contents of the canvas called "cnvs"
        replacing them with an updated view of the cells.
        the canvas is always double-buffered. Just create or modify
        canvas items as usual. When Tk returns to the event loop,
        the canvas is redrawn as soon as possible.
        http://mail.python.org/pipermail/python-list/2001-March/073778.html
        '''
        self.cnvs.delete(tk.ALL)
        list(map(self.place_cell_on_canvas, self.gol()))

    def iterate(self):
        self.change_go_now(False)
        self.gol.iterate()
        self.display()

    def go(self):
        if not self.go_now:
            self.go_stop()

    def stop(self):
        if self.go_now:
            self.go_stop()

    def go_stop(self):
        '''Must be implemented as a separate thread or check GUI for
        events at set intervals otherwise locks up.
        '''
        self.change_go_now()
        while self.go_now:
            self.gol.iterate()
            self.display()
            self.cnvs.update()
            # time.sleep(.1)

    def display_going_to_string(self):
        self.v_go_stop.set(going_to_string(self.go_now))

    def change_go_now(self, new_value=None):
        if new_value is None:
            self.go_now = not self.go_now
        else:
            self.go_now = bool(new_value)

        self.display_going_to_string()

    def random_if_unspecified_colour(self, colour=None):
        if colour is None:
            colour = colourutils.random_colour()
        return colour

    def print_colour(self, colour, is_foreground):
        print('%s Colour Changed To: %s' % (
            colour_type_to_string(is_foreground),
            colourutils.standard_hex_colour_padded(colour)))

    def change_foreground(self, colour=None):
        '''If Foreground colour is unspecified a random one will be chosen.
        '''
        colour = self.random_if_unspecified_colour(colour)
        tk_colour = colourutils.tk_hex_colour_padded(colour)

        self.print_colour(colour, is_foreground=True)
        self.cnvs.itemconfig(tk.ALL, fill=tk_colour)

        # storing choices
        self.foreground = colour
        self.foreground_tk_colour = tk_colour

    def change_background(self, colour=None):
        '''If Background colour is unspecified a random one will be chosen.
        '''
        colour = self.random_if_unspecified_colour(colour)
        tk_colour = colourutils.tk_hex_colour_padded(colour)

        self.print_colour(colour, is_foreground=False)
        self.cnvs.config(bg=tk_colour)

        # storing choices
        self.background = colour
        self.background_tk_colour = tk_colour

    def load_cells(self):
        try:
            cells = get_cells_from_file(file_cell_path)
        except IOError:
            print('File "%s" not found.' % file_cell_path)
        else:
            self.gol.cells = cells
            self.display()

    def canvas_resize(self, event):
        '''Change the size stored in the canvas when the window is
        resized so ChangeOriginDrag works properly.
        '''
        self.cnvs['width'], self.cnvs['height'] = event.width-2, event.height-2


if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()
