class Cabina:
    def __init__(self, codice, letti, ponte, prezzo_base):
        self.codice = codice
        self.letti = int(letti)
        self.ponte = ponte
        self._prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.tipo = "Standard" # Default, sovrascritto nelle sottoclassi

    def get_prezzo_finale(self):
        """Metodo per calcolare il prezzo, sovrascritto nelle sottoclassi."""
        return self._prezzo_base

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupata"
        prezzo = self.get_prezzo_finale()
        return f"{self.codice}: {self.tipo} | {self.letti} letti | Ponte {self.ponte} - Prezzo {prezzo:.2f}€ - {stato}"

    def __lt__(self, other):
        """Implementa il confronto per l'ordinamento per prezzo."""
        return self.get_prezzo_finale() < other.get_prezzo_finale()

    def __eq__(self, other):
        if isinstance(other, Cabina):
            return self.codice == other.codice
        return False

# --- Sottoclassi di Cabina ---

class CabinaConAnimali(Cabina):
    def __init__(self, codice, letti, ponte, prezzo_base, max_animali):
        super().__init__(codice, letti, ponte, prezzo_base)
        self.max_animali = int(max_animali)
        self.tipo = "Animali"

    def get_prezzo_finale(self):
        """Sovrapprezzo del 10% per ogni animale ammesso."""
        sovrapprezzo_percentuale = 1 + (0.10 * self.max_animali)
        return self._prezzo_base * sovrapprezzo_percentuale

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupata"
        prezzo = self.get_prezzo_finale()
        base_str = f"{self.codice}: {self.tipo} | {self.letti} letti | Ponte {self.ponte} - Prezzo {prezzo:.2f}€"
        return f"{base_str} - Max animali: {self.max_animali} - {stato}"

class CabinaDeluxe(Cabina):
    def __init__(self, codice, letti, ponte, prezzo_base, specifica):
        super().__init__(codice, letti, ponte, prezzo_base)
        self.specifica = specifica
        self.tipo = "Deluxe"

    def get_prezzo_finale(self):
        """Sovrapprezzo fisso del 20%."""
        return self._prezzo_base * 1.20

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupata"
        prezzo = self.get_prezzo_finale()
        base_str = f"{self.codice}: {self.tipo} ({self.specifica}) | {self.letti} letti | Ponte {self.ponte} - Prezzo {prezzo:.2f}€"
        return f"{base_str} - {stato}"