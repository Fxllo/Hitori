import g2d
from boardgame import BoardGame

W, H = 60, 60
CELL_SIZE = 60
DECORATIVE_BORDER_WIDTH = 5
SEPARATOR_BORDER_WIDTH = 5
status_rect_height = 50
DECORATIVE_BORDER_COLOR = (248, 236, 194)
SEPARATOR_BORDER_COLOR = (0, 0, 0)
CLEAR_CELL_COLOR = (204, 204, 204)
DARK_CELL_COLOR = (0, 0, 0)
ALONE_CELL_COLOR = (255, 204, 204)
ADJAENT_CELL_COLOR = (255, 0, 0)
CIRCLE_CELL_COLOR = (0, 255, 0)

class HitoriGui:
    def __init__(self, game: BoardGame):
        self._game = game
        self._cols = game.cols()
        self._rows = game.rows()
        self._width = self._cols * W + 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
        self._height = self._rows * H + 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
        self._grid_size = max(self._cols, self._rows)
        g2d.init_canvas((self._width, self._height + status_rect_height))
        self._error = False
        self._errorArea = False
        self._game_finished = False
        self._grid = {(row, col): {"value": game._numbers[row * self._cols + col], "state": "clear", "buffer": False} 
              for row in range(self._rows) for col in range(self._cols)}

    def tick(self):
        g2d.clear_canvas()

        g2d.set_color(DECORATIVE_BORDER_COLOR)
        g2d.draw_rect((0, 0), (self._width, self._height))
        g2d.set_color(SEPARATOR_BORDER_COLOR)
        g2d.draw_rect(
            (DECORATIVE_BORDER_WIDTH, DECORATIVE_BORDER_WIDTH),
            (self._width - 2 * DECORATIVE_BORDER_WIDTH, self._height - 2 * DECORATIVE_BORDER_WIDTH)
        )

        for row in range(self._rows):
            for col in range(self._cols):
                x = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + col * CELL_SIZE
                y = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + row * CELL_SIZE
                cell = self._grid[(row, col)]
                if cell["state"] == "dark":
                    g2d.set_color(DARK_CELL_COLOR)
                elif cell["state"] == "alone":
                    g2d.set_color(ALONE_CELL_COLOR)
                elif cell["state"] == "adjacent":
                    g2d.set_color(ADJAENT_CELL_COLOR)
                elif cell["state"] == "circle":
                    g2d.set_color(CIRCLE_CELL_COLOR)
                else:
                    g2d.set_color(CLEAR_CELL_COLOR)
                
                g2d.draw_rect((x, y), (CELL_SIZE, CELL_SIZE))

                g2d.set_color((255, 255, 255) if cell["state"] in ["dark", "adjacent"] else (0, 0, 0))
                g2d.draw_text(str(cell["value"]), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 20)
                g2d.draw_text(str(cell["state"]), (x + CELL_SIZE // 2, y + CELL_SIZE // 2 + 10), 20)

        g2d.set_color((0, 0, 0))
        PLAY_AREA_SIZE = self._width - 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
        for i in range(self._grid_size + 1):
            g2d.draw_line(
                (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE),
                (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + PLAY_AREA_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE),
                2
            )
            g2d.draw_line(
                (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH),
                (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + PLAY_AREA_SIZE),
                2
            )

        self.display_status()

        if g2d.mouse_clicked():
            row, col = self.get_mouse_cell()
            print(f"Prima di play: {self._grid[(row, col)]['state']}")
            self._game.play(row, col, self._grid)
            print(f"Dopo play: {self._grid[(row, col)]['state']}")
            self.check_adjacent(row, col)
            self.closedAreas()
        elif g2d.key_pressed("Escape"):
            g2d.close_canvas()
        elif g2d.mouse_right_clicked():
            row, col = self.get_mouse_cell()
            if self.is_within_grid(row, col):
                cell = self._grid[(row, col)]
                if cell["state"] == "dark":
                    self.darken_adjacent_cells(row, col)
            self.check_adjacent(row, col)
            self.closedAreas()
                
            if self._game_finished:
                self.display_status()
                g2d.main_loop(None)
            if self._game.finished(self.wrong()):
                self._game_finished = True
        
    def wrong(self):
        return self._error or self._errorArea
        
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
            self._grid[c]["state"] = "clear"

    def display_status(self):
        status_text = self._game.status(self.wrong())
        g2d.set_color((204, 204, 204))
        g2d.draw_rect((0, self._height), (self._width, status_rect_height))
        g2d.set_color((0, 0, 0))
        g2d.draw_text(status_text, (self._width // 2, self._height + status_rect_height // 2.5), 30)
        
    def get_mouse_cell(self):
        mouse_x, mouse_y = g2d.mouse_pos()
        col = (mouse_x - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        row = (mouse_y - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        return row, col
    
    def is_within_grid(self, row, col):
        return 0 <= col < self._cols and 0 <= row < self._rows
    
    def darken_adjacent_cells(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if self.is_within_grid(nr, nc):
                self._grid[(nr, nc)]["state"] = "dark"

def gui_play(game: BoardGame):
    gui = HitoriGui(game)
    g2d.main_loop(gui.tick)