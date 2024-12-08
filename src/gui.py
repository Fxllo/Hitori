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
        self._grid_size = game.grid_size()
        self._width = self._cols * W + 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
        self._height = self._rows * H + 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
        g2d.init_canvas((self._width, self._height + status_rect_height))
        self._game_finished = False

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
                cell = self._game.grid()[(row, col)]
                if cell["state"] == "dark":
                    g2d.set_color(DARK_CELL_COLOR)
                elif cell["state"] == "alone":
                    g2d.set_color(ALONE_CELL_COLOR)
                elif cell["state"] == "adjacent":
                    g2d.set_color(ADJAENT_CELL_COLOR)
                else:
                    g2d.set_color(CLEAR_CELL_COLOR)
                
                g2d.draw_rect((x, y), (CELL_SIZE, CELL_SIZE))

                if cell["state"] == "circle":
                    g2d.set_color(CIRCLE_CELL_COLOR)
                    g2d.draw_circle((x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
                
                g2d.set_color((0, 0, 0))
                g2d.draw_text(str(cell["value"]), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 20)

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
                
        if self._game_finished:
            self.display_status()
            g2d.alert("Hai finito il gioco!")
            g2d.main_loop(None)
            return
            
        self._game.play(self)
        
        if self._game.finished(self._game.wrong()):
            self._game_finished = True
            
        self.display_status()
        
    def display_status(self):
        status_text = self._game.status(self._game.wrong())
        g2d.set_color((204, 204, 204))
        g2d.draw_rect((0, self._height), (self._width, status_rect_height))
        g2d.set_color((0, 0, 0))
        g2d.draw_text(status_text, (self._width // 2, self._height + status_rect_height // 2.5), 30)
        
    def get_mouse_cell(self):
        mouse_x, mouse_y = g2d.mouse_pos()
        col = (mouse_x - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        row = (mouse_y - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        return row, col

def gui_play(game: BoardGame):
    gui = HitoriGui(game)
    g2d.main_loop(gui.tick)