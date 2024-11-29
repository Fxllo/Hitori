import g2d
import random

# Definizione dei parametri
GRID_SIZE = 7  # Griglia 7x7
WINDOW_SIZE = 400  # Dimensione totale della finestra
DECORATIVE_BORDER_WIDTH = 5  # Spessore del bordo decorativo
SEPARATOR_BORDER_WIDTH = 5  # Spessore del bordo nero tra decorazione e campo
PLAY_AREA_SIZE = WINDOW_SIZE - 2 * (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH)  # Area di gioco
CELL_SIZE = PLAY_AREA_SIZE // GRID_SIZE  # Dimensione di ogni cella

# Creazione della griglia
# value = numero nella cella
# state = "clear" (cella numerica, bianca), "dark" (cella oscuratra, nera), "adjacent" (celle oscurate adiacenti, rosso), "alone" (cella numerica isolata, rosso chiaro)
grid = {(row, col): {"value": random.randint(1, 9), "state": "clear"} for row in range(GRID_SIZE) for col in range(GRID_SIZE)}

def tick():
    g2d.clear_canvas()
    
    # Disegna il bordo decorativo
    DECORATIVE_BORDER_COLOR = (248, 236, 194)
    g2d.set_color(DECORATIVE_BORDER_COLOR)
    g2d.draw_rect((0, 0), (WINDOW_SIZE, WINDOW_SIZE))
    
    # Disegna il bordo separatore nero
    SEPARATOR_BORDER_COLOR = (0, 0, 0)
    g2d.set_color(SEPARATOR_BORDER_COLOR)
    g2d.draw_rect(
        (DECORATIVE_BORDER_WIDTH, DECORATIVE_BORDER_WIDTH),
        (WINDOW_SIZE - 2 * DECORATIVE_BORDER_WIDTH, WINDOW_SIZE - 2 * DECORATIVE_BORDER_WIDTH)
    )
    
    # Disegna la griglia all'interno del bordo separatore
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + col * CELL_SIZE
            y = DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + row * CELL_SIZE

            # Colore della cella in base al suo stato
            if grid[(row, col)]["state"] == "dark":
                g2d.set_color((0, 0, 0))  # Oscurata: grigio
            elif grid[(row, col)]["state"] == "alone":
                g2d.set_color((150, 0, 0))
            elif grid[(row, col)]["state"] == "adjacent":
                g2d.set_color((255, 0, 0))
            else:
                g2d.set_color((255, 255, 255))  # Normale: bianco
            g2d.draw_rect((x, y), (CELL_SIZE, CELL_SIZE))
            
            # Disegna il numero al centro della cella
            g2d.set_color((0, 0, 0))
            g2d.draw_text(str(grid[(row, col)]["value"]), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 20)
    
    # Disegna le linee della griglia
    g2d.set_color((0, 0, 0))  # Nero per le linee
    for i in range(GRID_SIZE + 1):
        # Linee orizzontali
        g2d.draw_line(
            (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE),
            (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + PLAY_AREA_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE),
            2
        )
        # Linee verticali
        g2d.draw_line(
            (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH),
            (DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + i * CELL_SIZE, DECORATIVE_BORDER_WIDTH + SEPARATOR_BORDER_WIDTH + PLAY_AREA_SIZE),
            2
        )
    
    # Gestisci click del mouse per cambiare stato della cella
    if g2d.mouse_clicked():
        mouse_x, mouse_y = g2d.mouse_pos()
        col = (mouse_x - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        row = (mouse_y - DECORATIVE_BORDER_WIDTH - SEPARATOR_BORDER_WIDTH) // CELL_SIZE
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            grid[(row, col)]["state"] = "dark" if grid[(row, col)]["state"] == "clear" else "clear"
        check_adjacent(row, col)

#Controllo che le celle nere non siano adiacenti verticalmente o orizzontalmente
def check_adjacent(row, col):
    if grid[(row, col)]["state"] == "dark":
        if row > 0 and (grid[(row - 1, col)]["state"] == "dark" or grid[(row - 1, col)]["state"] == "adjacent"):
            grid[((row, col))]["state"] = "adjacent"
            check_adjacent(row - 1, col)
        if row < GRID_SIZE - 1 and (grid[(row + 1, col)]["state"] == "dark" or grid[(row + 1, col)]["state"] == "adjacent"):
            grid[(row, col)]["state"] = "adjacent"
            check_adjacent(row + 1, col)
        if col > 0 and (grid[(row, col - 1)]["state"] == "dark" or grid[(row, col - 1)]["state"] == "adjacent"):
            grid[(row, col)]["state"] = "adjacent"
            check_adjacent(row, col - 1)
        if col < GRID_SIZE - 1 and (grid[(row, col + 1)]["state"] == "dark" or grid[(row, col + 1)]["state"] == "adjacent"):
            grid[(row, col)]["state"] = "adjacent"
            check_adjacent(row, col + 1)
    elif grid[(row, col)]["state"] == "clear":
        if row > 0 and grid[(row - 1, col)]["state"] == "adjacent":
            grid [(row-1, col)]["state"] = "dark"
            check_adjacent(row - 1, col)
        if row < GRID_SIZE - 1 and grid[(row + 1, col)]["state"] == "adjacent":
            grid [(row+1, col)]["state"] = "dark"
            check_adjacent(row + 1, col)
        if col > 0 and grid[(row, col - 1)]["state"] == "adjacent":
            grid [(row, col-1)]["state"] = "dark"
            check_adjacent(row, col - 1)
        if col < GRID_SIZE - 1 and grid[(row, col + 1)]["state"] == "adjacent":
            grid [(row, col+1)]["state"] = "dark"
            check_adjacent(row, col + 1)

def main():
    g2d.init_canvas((WINDOW_SIZE, WINDOW_SIZE))
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()