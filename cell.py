from tkinter import Button
from tkinter import Label
import settings
import random

class Cell:
    all = []
    mines_left = settings.MINES_COUNT
    mines_left_label = None
    game_over = False
    info_frame = None


    def __init__(self, x, y, is_mine = False, is_displayed = False, is_flagged = False):
        self.is_displayed = is_displayed
        self.is_mine = is_mine
        self.is_flagged = is_flagged
        self.cell_btn_object = None
        
        self.x = x
        self.y = y
        Cell.all.append(self)

    @staticmethod
    def create_label(location):
        Cell.info_frame = location

        lbl = Label(location, text = str(Cell.mines_left))

        Cell.mines_left_label = lbl

        lbl.place(x = 0, y = 0)

    def create_btn_object(self, location):


        btn = Button(
            location,
            bg = "gray",
            width = settings.CELL_WIDTH,
            height = settings.CELL_HEIGHT,
            #text = f'{self.x}, {self.y}'
        )

        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)

        self.cell_btn_object = btn

    def left_click_actions(self, event):
        if not Cell.game_over:
            if self.is_mine:
                self.show_mines()

            else:
                self.show_cell()

    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

        return None

    def get_neighbors(self):

        neighbors = []

        neighbors.append(self.get_cell(self.x - 1, self.y))
        neighbors.append(self.get_cell(self.x - 1, self.y - 1))
        neighbors.append(self.get_cell(self.x, self.y - 1))
        neighbors.append(self.get_cell(self.x + 1, self.y - 1))
        neighbors.append(self.get_cell(self.x + 1, self.y))
        neighbors.append(self.get_cell(self.x + 1, self.y + 1))
        neighbors.append(self.get_cell(self.x, self.y + 1))
        neighbors.append(self.get_cell(self.x - 1, self.y + 1))

        return neighbors

    def get_surrounding_mines(self):

        surrounding_mines = 0

        for c in self.get_neighbors():
            if c and c.is_mine:
                surrounding_mines += 1

        return surrounding_mines

    def show_cell(self):

        if not self.is_displayed:

            self.is_displayed = True

            mines = self.get_surrounding_mines()

            if mines == 0:
                self.show_neighbors()
                self.cell_btn_object.configure(bg = "white")
                mines = ""

            else:
                self.cell_btn_object.configure(bg = "gray")
            
            self.cell_btn_object.configure(text = f'{mines}')

            if self.is_flagged:
                self.is_flagged = False
                Cell.mines_left += 1

    def show_neighbors(self):
        neighbors = self.get_neighbors()
        for c in neighbors:
            if c:                    
                c.show_cell()

    def show_mines(self):
        
        Cell.game_over = True

        for c in Cell.all:
            if c.is_mine:
                c.cell_btn_object.configure(bg = "red")
                c.is_displayed = True
            else:
                c.show_cell()

        Cell.game_end()

    
    def right_click_actions(self, event):
        if not Cell.game_over:
            if self.is_flagged:
                self.cell_btn_object.configure(bg = "gray", text = "")
                Cell.mines_left += 1
                Cell.mines_left_label.configure(text = str(Cell.mines_left))
                self.is_flagged = False
            elif not self.is_displayed:
                self.cell_btn_object.configure(bg = "green", text = "!")
                Cell.mines_left -= 1
                Cell.mines_left_label.configure(text = str(Cell.mines_left))
                self.is_flagged = True        
                

    @staticmethod
    def randomize_mines():
        mines = random.sample(Cell.all, settings.MINES_COUNT)
        for mine in mines:
            mine.is_mine = True
            

    @staticmethod
    def find_starting_place():

        safe_places = []

        for cell in Cell.all:
            if cell.get_surrounding_mines() == 0 and not cell.is_mine:
                safe_places.append(cell)

        random.choice(safe_places).show_cell()

    @staticmethod
    def game_end():

        lbl = Label(
            Cell.info_frame,
            text = "Game Over!"
        )

        lbl.place(x = 570, y = 0)
        

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'