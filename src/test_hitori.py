import unittest
from hitori import Hitori

class TestHitori(unittest.TestCase):
    def setUp(self):
        self.hitori = Hitori("./src/hitoriTables/5-easy.csv")

    def test_no_repeated_numbers(self):
        """Verifica che non ci siano numeri ripetuti tra quelli non anneriti."""
        self.hitori.testPlay(0, 0)
        self.hitori.testPlay(1, 1)
        self.hitori.testPlay(4, 0)
        self.hitori.testPlay(3, 1)
        self.hitori.testPlay(3, 3)
        self.hitori.testPlay(2, 4)
        self.hitori.testPlay(0, 4)

        wrong = self.hitori.wrong()
        self.assertTrue(self.hitori.finished(wrong))

    def test_no_adjacent_dark_cells(self):
        """Verifica che non ci siano celle annerite adiacenti."""
        self.hitori.testPlay(0, 0)
        self.hitori.testPlay(0, 1)
        
        wrong = self.hitori.wrong()
        self.assertFalse(self.hitori.finished(wrong))

    def test_contiguous_white_cells(self):
        """Verifica la contiguità delle celle bianche."""
        self.hitori.testPlay(0, 0)  # Annerisce una cella
        self.hitori.testPlay(2, 2)  # Annerisce una cella lontana

        wrong = self.hitori.wrong()
        self.assertFalse(self.hitori.finished(wrong))

    def test_game_completion(self):
        """Verifica se il gioco è completato correttamente."""
        self.hitori.testPlay(0, 0)
        self.hitori.testPlay(1, 1)
        self.hitori.testPlay(4, 0)
        self.hitori.testPlay(3, 1)
        self.hitori.testPlay(3, 3)
        self.hitori.testPlay(2, 4)
        self.hitori.testPlay(0, 4)

        wrong = self.hitori.wrong()
        self.assertEqual(self.hitori.status(wrong), "Completed!")

    def test_read_function(self):
        """Verifica la funzione read."""
        self.assertEqual(self.hitori.read(0, 0), self.hitori._numbers[0])

if __name__ == "__main__":
    unittest.main()