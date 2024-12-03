from boardgame import BoardGame

class Hitori(BoardGame):
    def __init__(self, filename):
        self._numbers = self.load_matrix_from_csv(filename)
        self._w = self._h = int(len(self._numbers) ** 0.5)
        self._annots = [0] * (self._w * self._h)

    def load_matrix_from_csv(self, filename):
        matrix = []
        with open(filename, mode='r') as file:
            import csv
            reader = csv.reader(file)
            for row in reader:
                matrix.extend([int(x) for x in row])
        return matrix

    def finished(self, wrong: bool) -> bool:
        if wrong:
            return False

        seen_row = [set() for _ in range(self._h)]
        seen_col = [set() for _ in range(self._w)]

        for i in range(self._w * self._h):
            if self._annots[i] == 0:
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
    
    def play(self, row: int, col: int, grid: dict):
        if 0 <= col < self.cols() and 0 <= row < self.rows():
            cell = grid[(row, col)]
            if cell["state"] == "clear" or cell["state"] == "alone":
                cell["state"] = "dark"
                self._annots[row * self.cols() + col] = 1
            else:
                cell["state"] = "clear"
                self._annots[row * self.cols() + col] = 0
    
    def read(self, row: int, col: int) -> int:
        return self._numbers[row * self.cols() + col]