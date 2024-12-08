from boardgame import BoardGame
import g2d
import random
from gui import HitoriGui

class Hitori(BoardGame):
    def __init__(self, filename):
        self._grid = {}
        self._numbers = self.load_matrix_from_csv(filename)
        self._w = self._h = int(len(self._numbers) ** 0.5)
        self._grid_size = max(self.cols(), self.rows())
        self._annots = [0] * (self._w * self._h)
        self._error = False
        self._errorArea = False
        self._lastAction = None


    def load_matrix_from_csv(self, filename):
        matrix = []
        with open(filename, mode='r') as file:
            import csv
            reader = csv.reader(file)
            y = 0
            for row in reader:
                for x in range(len(row)):
                    matrix.extend([int(row[x])])
                    self._grid[(y, x)] = {"value": int(row[x]), "state": "clear"}
                y += 1
        return matrix

    def finished(self, wrong: bool) -> bool:
        if wrong:
            return False

        seen_row = [set() for _ in range(self._h)]
        seen_col = [set() for _ in range(self._w)]

        for i in range(self._w * self._h):
            if self._annots[i] == 0 or self._annots[i] == 2:
                number = self._numbers[i]
                row = i // self._w
                col = i % self._w
                if number in seen_row[row]:
                    return False
                seen_row[row].add(number)

                if number in seen_col[col]:
                    return False
                seen_col[col].add(number)
        return True

    def status(self, wrong: bool) -> str:
        if wrong:
            return "Error"
        return "Completed!" if self.finished(wrong) else "Playing"

    def cols(self):
        return self._w

    def rows(self):
        return self._h

    def grid_size(self):
        return self._grid_size
    
    def wrong(self):
        return self._error or self._errorArea
    
    def play(self, gui: HitoriGui):
        rows = self.rows()
        cols = self.cols()
        if g2d.mouse_clicked():
            row, col = gui.get_mouse_cell()
            if self.is_within_grid(row, col):
                cell = self._grid[(row, col)]
                match cell["state"]:
                    case "clear" | "alone":
                        cell["state"] = "dark"
                        self._annots[row * cols + col] = 1
                    case "dark":
                        cell["state"] = "circle"
                        self._annots[row * cols + col] = 2
                    case "circle" | "adjacent":
                        cell["state"] = "clear"
                        self._annots[row * cols + col] = 0
                        
                self._grid[(row, col)]["state"] = cell["state"]
                self.check_adjacent(row, col)
                self.closedAreas()
        elif g2d.key_pressed("Escape"):
            g2d.close_canvas()
        elif g2d.key_pressed("h"):
            if self._lastAction == "dark":
                for (row, col), data in self._grid.items():
                    if data["state"] == "dark":
                        self.darken_adjacent_cells(row, col)
            elif self._lastAction == "circle":
                for row in range(rows):
                    for col in range(cols):
                        if self._grid[(row, col)]["state"] == "circle":
                            self.circleSameNumber(row, col)
                for row in range(rows):
                    for col in range(cols):
                        self.check_adjacent(row, col)
                self.closedAreas()
        elif g2d.key_pressed("a"):
            self.findNextMove()
        elif g2d.mouse_right_clicked():
            row, col = gui.get_mouse_cell()
            if self.is_within_grid(row, col):
                cell = self._grid[(row, col)]
                if cell["state"] == "dark":
                    self.darken_adjacent_cells(row, col)
                elif cell["state"] == "circle":
                    self.circleSameNumber(row, col)
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                    nr, nc = row + dr, col + dc
                    if self.is_within_grid(nr, nc):
                        self.check_adjacent(nr, nc)
            self.closedAreas()
    
    def read(self, row: int, col: int) -> int:
        return self._numbers[row * self.cols() + col]
    
    def grid(self) -> dict:
        return self._grid
    
    def check_adjacent(self, row, col):
        if self._grid[(row, col)]["state"] == "dark":
            if row > 0 and (self._grid[(row - 1, col)]["state"] == "dark" or self._grid[(row - 1, col)]["state"] == "adjacent"):
                self._grid[((row, col))]["state"] = "adjacent"
                self._error = True
                self.check_adjacent(row - 1, col)
            if row < self._grid_size - 1 and (self._grid[(row + 1, col)]["state"] == "dark" or self._grid[(row + 1, col)]["state"] == "adjacent"):
                self._grid[(row, col)]["state"] = "adjacent"
                self._error = True
                self.check_adjacent(row + 1, col)
            if col > 0 and (self._grid[(row, col - 1)]["state"] == "dark" or self._grid[(row, col - 1)]["state"] == "adjacent"):
                self._grid[(row, col)]["state"] = "adjacent"
                self._error = True
                self.check_adjacent(row, col - 1)
            if col < self._grid_size - 1 and (self._grid[(row, col + 1)]["state"] == "dark" or self._grid[(row, col + 1)]["state"] == "adjacent"):
                self._grid[(row, col)]["state"] = "adjacent"
                self._error = True
                self.check_adjacent(row, col + 1)
        elif self._grid[(row, col)]["state"] == "clear":
            if row > 0 and self._grid[(row - 1, col)]["state"] == "adjacent":
                self._grid [(row-1, col)]["state"] = "dark"
                self._error = False
                self.check_adjacent(row - 1, col)
            if row < self._grid_size - 1 and self._grid[(row + 1, col)]["state"] == "adjacent":
                self._grid [(row+1, col)]["state"] = "dark"
                self._error = False
                self.check_adjacent(row + 1, col)
            if col > 0 and self._grid[(row, col - 1)]["state"] == "adjacent":
                self._grid [(row, col-1)]["state"] = "dark"
                self._error = False
                self.check_adjacent(row, col - 1)
            if col < self._grid_size - 1 and self._grid[(row, col + 1)]["state"] == "adjacent":
                self._grid [(row, col+1)]["state"] = "dark"
                self._error = False
                self.check_adjacent(row, col + 1)

    def closedAreas(self):
        visited = set()
        non_dark_cells = {(row, col) for row in range(self._grid_size) for col in range(self._grid_size) 
                        if not (self._grid[(row, col)]["state"] == "dark" or self._grid[(row, col)]["state"] == "adjacent")}
        if not non_dark_cells:
            return
        stack = [next(iter(non_dark_cells))]
        while stack:
            cell = stack.pop()
            if cell not in visited:
                visited.add(cell)
                row, col = cell
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dr, col + dc
                    if (nr, nc) in non_dark_cells and (nr, nc) not in visited:
                        stack.append((nr, nc))
        if non_dark_cells - visited:
            self._errorArea = True
        else:
            self._errorArea = False

        for c in non_dark_cells - visited:
            self._grid[c]["state"] = "alone"
        for c in visited:
            self._grid[c]["state"] = "clear" if self._grid[c]["state"] == "alone" else self._grid[c]["state"]
            
    def darken_adjacent_cells(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if self.is_within_grid(nr, nc):
                self._grid[(nr, nc)]["state"] = "circle"
        self._lastAction = "dark"
    
    def circleSameNumber(self, row, col):
        number = self.read(row, col)
        for r in range(self.rows()):
            if r != row and self._grid[(r, col)]["value"] == number:
                self._grid[(r, col)]["state"] = "dark"
        for c in range(self.cols()):
            if c != col and self._grid[(row, c)]["value"] == number:
                self._grid[(row, c)]["state"] = "dark"
        self._lastAction = "circle"
                
    def is_within_grid(self, row, col):
        return 0 <= col < self.cols() and 0 <= row < self.rows()
    
    def findNextMove(self):
        available_cells = [(r, c) for r in range(self.rows()) for c in range(self.cols()) if self._grid[(r, c)]["state"] == "clear"]
        if not available_cells:
            return
        row, col = random.choice(available_cells)
        randMove = random.choice([0, 1])
        if randMove:
            self._grid[(row, col)]["state"] = "dark"
            self.darken_adjacent_cells(row, col)
            if self.wrong():
                self._grid[(row, col)]["state"] = "circle"
            self.check_adjacent(row, col)
        else:
            self._grid[(row, col)]["state"] = "circle"
            self.circleSameNumber(row, col)
            if self.wrong():
                self._grid[(row, col)]["state"] = "dark"
            self.check_adjacent(row, col)

        self.closedAreas()