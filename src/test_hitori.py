import unittest
from hitori import Hitori

class TestHitori(unittest.TestCase):
    def setUp(self):
        self.hitori = Hitori("./src/hitoriTables/5-easy.csv")

    def test_no_repeated_numbers(self):
        """Verifica che non ci siano numeri ripetuti tra quelli non anneriti."""
        self.hitori.play(0, 4, {"state": "dark"})
        self.hitori.play(1, 1, {"state": "dark"})
        self.hitori.play(1, 3, {"state": "dark"})
        self.hitori.play(2, 0, {"state": "dark"})
        self.hitori.play(3, 3, {"state": "dark"})
        self.hitori.play(4, 0, {"state": "dark"})
        self.hitori.play(4, 4, {"state": "dark"})

        self.assertTrue(self.hitori.finished(wrong=False))

    def test_no_adjacent_dark_cells(self):
        """Verifica che non ci siano celle annerite adiacenti."""
        self.hitori.play(0, 0, {"state": "dark"})
        self.hitori.play(0, 1, {"state": "dark"})
        self.assertFalse(self.hitori.finished(wrong=True))

    def test_contiguous_white_cells(self):
        """Verifica la contiguità delle celle bianche."""
        self.hitori.play(0, 0, {"state": "dark"})  # Annerisce una cella
        self.hitori.play(2, 2, {"state": "dark"})  # Annerisce una cella lontana

        self.assertFalse(self.hitori.finished(wrong=True))

    def test_game_completion(self):
        """Verifica se il gioco è completato correttamente."""
        self.hitori.play(0, 4, {"state": "dark"})
        self.hitori.play(1, 1, {"state": "dark"})
        self.hitori.play(1, 3, {"state": "dark"})
        self.hitori.play(2, 0, {"state": "dark"})
        self.hitori.play(3, 3, {"state": "dark"})
        self.hitori.play(4, 0, {"state": "dark"})
        self.hitori.play(4, 4, {"state": "dark"})
        
        self.assertEqual(self.hitori.status(wrong=False), "Completed!")

    def test_read_function(self):
        """Verifica la funzione read."""
        self.assertEqual(self.hitori.read(0, 0), self.hitori._numbers[0])

if __name__ == "__main__":
    unittest.main()