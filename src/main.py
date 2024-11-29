import g2d
import random

# Definizione dei parametri
GRID_SIZE = 7
WINDOW_SIZE = 400
DECORATIVE_BORDER_WIDTH = 5
SEPARATOR_BORDER_WIDTH = 5
PLAY_AREA_SIZE = WINDOW_SIZE - 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)
CELL_SIZE = PLAY_AREA_SIZE // GRID_SIZE

grid = {(row, col): {"value": random.randint(1, 9), "dark": False} for row in range(GRID_SIZE) for col in range(GRID_SIZE)}

def closedAreas():
    visited = set()
    non_dark_cells = {(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if not grid[(row, col)]["dark"]}

    if not non_dark_cells:
        return True

    start_cell = next(iter(non_dark_cells))

    stack = [start_cell]
    while stack:
        cell = stack.pop()
        if cell not in visited:
            visited.add(cell)
            row, col = cell
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if (nr, nc) in non_dark_cells and (nr, nc) not in visited:
                    stack.append((nr, nc))
    return visited == non_dark_cells

def tick():
    global state
    
    g2d.clear_canvas()
    
    DECORATIVE_BORDER_COLOR = (248, 236, 194)
    g2d.set_color(DECORATIVE_BORDER_COLOR)
    g2d.draw_rect((0, 0), (WINDOW_SIZE, WINDOW_SIZE))
    
    SEPARATOR_BORDER_COLOR = (0, 0, 0)
    g2d.set_color(SEPARATOR_BORDER_COLOR)
    g2d.draw_rect(
        (DECORATIVE_BORDER_WIDTH, DECORATIVE_BORDER_WIDTH),
        (WINDOW_SIZE - 2 * DECORATIVE_BORDER_WIDTH, WINDOW_SIZE - 2 * DECORATIVE_BORDER_WIDTH)
    )
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + col * CELL_SIZE
            y = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + row * CELL_SIZE

            if grid[(row, col)]["dark"]:
                g2d.set_color((0, 0, 0))
            else:
                g2d.set_color((204, 204, 204))
            g2d.draw_rect((x, y), (CELL_SIZE, CELL_SIZE))
            
            g2d.set_color((0, 0, 0))
            g2d.draw_text(str(grid[(row, col)]["value"]), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 20)
    

    g2d.set_color((0, 0, 0))
    for i in range(GRID_SIZE + 1):
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
    
    if g2d.mouse_clicked():
        mouse_x, mouse_y = g2d.mouse_pos()
        col = (mouse_x - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        row = (mouse_y - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            grid[(row, col)]["dark"] = not grid[(row, col)]["dark"]
    
    if not closedAreas():
        print("Area closed!")
        
def main():
    g2d.init_canvas((WINDOW_SIZE, WINDOW_SIZE))
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()