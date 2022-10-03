from tkinter import *
import settings
import utils
from cell import Cell

r = Tk()

#Override the settings of the window
r.configure(bg = "black")

r.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
r.title("Minesweeper")
r.resizable(False, False)


top_frame = Frame(
    r,
    bg = "red",
    width = settings.WIDTH, 
    height = utils.height_prct(5))

top_frame.place(x=0, y=0)

# left_frame = Frame(
#     r,
#     bg = "blue",
#     width = utils.width_prct(25),
#     height = utils.height_prct(75)
# )

# left_frame.place(x=0, y = utils.height_prct(25))

center_frame = Frame(
    r,
    bg = "green",
    width = utils.width_prct(100),#75),
    height = utils.height_prct(95)#75)
)

center_frame.place(x=0, y=utils.height_prct(5))#x=utils.width_prct(25), y=utils.height_prct(25))

for x in range(settings.X_AXIS):
    for y in range(settings.Y_AXIS):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column = x, row = y)


Cell.randomize_mines()
Cell.find_starting_place()
Cell.create_label(top_frame)


r.mainloop()
