from abc import ABC, abstractmethod

class BoardGame(ABC):
    """Classe astratta che rappresenta un gioco basato su griglie."""
    
    @abstractmethod
    def cols(self) -> int:
        """Restituisce il numero di colonne nella griglia."""
        pass

    @abstractmethod
    def rows(self) -> int:
        """Restituisce il numero di righe nella griglia."""
        pass

    @abstractmethod
    def finished(self) -> bool:
        """
        Determina se il gioco è terminato.
        
        Returns:
            bool: True se il gioco è completato, altrimenti False.
        """
        pass

    @abstractmethod
    def status(self) -> str:
        """
        Restituisce un messaggio che descrive lo stato del gioco.
        
        Returns:
            str: Stato corrente del gioco (es. "Playing", "Completed").
        """
        pass
    
    @abstractmethod
    def play(self, row: int, col: int):
        """
        Esegue una mossa nella posizione specificata.
        
        Args:
            row (int): Indice di riga.
            col (int): Indice di colonna.
        """
        pass
    
    @abstractmethod
    def read(self, row: int, col: int) -> int:
        """
        Restituisce il valore nella posizione specificata.
        
        Args:
            row (int): Indice di riga.
            col (int): Indice di colonna.
        
        Returns:
            int: Valore nella posizione specificata.
        """
        pass