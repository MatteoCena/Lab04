class Passeggero:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self._cabina_assegnata = None

    @property
    def cabina_assegnata(self):
        return self._cabina_assegnata

    @cabina_assegnata.setter
    def cabina_assegnata(self, cabina):
        self._cabina_assegnata = cabina

    def __str__(self):
        return f"Passeggero {self.codice}: {self.nome} {self.cognome}"

    def __eq__(self, other):
        if isinstance(other, Passeggero):
            return self.codice == other.codice
        return False