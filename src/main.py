def main():
    from gui import gui_play
    from hitori import Hitori
    from g2d import prompt, alert
    
    levelNames = {
        5: "5-easy.csv",
        6: "6-medium.csv",
        8: "8-hard.csv",
        9: "9-veryhard.csv",
        12: "12-superhard.csv",
        15: "15-impossible.csv"
    }
    
    while True:
        try:
            level = int(prompt("Enter difficulty: "))
            if level in levelNames:
                level = "./src/hitoriTables/" + levelNames[level]
                break
            else:
                alert("Invalid level selected")
        except ValueError:
            alert("Please enter a valid number for difficulty level.")
    
    game = Hitori(filename=level)
    gui_play(game)

if __name__ == "__main__":
    main()
    