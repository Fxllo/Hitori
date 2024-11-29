def main():
    from gui import gui_play
    from hitori import Hitori
    game = Hitori(filename="hitori.csv")
    gui_play(game)

if __name__ == "__main__":
    main()