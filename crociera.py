class Crociera:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.cabine = {}
        self.passeggeri = {}
        self.prenotazioni = {}

    # --- Setter e Getter ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def _crea_oggetto_cabina(self, riga):
        """Metodo di utilità per creare l'oggetto Cabina corretto."""
        codice, letti, ponte, prezzo_base, *extra = riga

        if not extra:
            # 4 campi presenti (codice, letti, ponte, prezzo_base) -> Cabina Standard
            return Cabina(codice, letti, ponte, prezzo_base)

        campo_aggiuntivo = extra[0]

        try:
            # Se il campo aggiuntivo è un numero -> Cabina con Animali
            max_animali = int(campo_aggiuntivo)
            return CabinaConAnimali(codice, letti, ponte, prezzo_base, max_animali)
        except ValueError:
            # Altrimenti è una stringa -> Cabina Deluxe
            specifica = campo_aggiuntivo
            return CabinaDeluxe(codice, letti, ponte, prezzo_base, specifica)






    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        if not exists(file_path):
            raise FileNotFoundError(f"Errore: File non trovato al percorso specificato: {file_path}")

        with open(file_path, 'r') as file:
            lettore = csv.reader(file)
            for riga in lettore:
                if not riga:
                    continue

                codice = riga[0]

                if codice.startswith('CAB'):
                    # Riga relativa a una Cabina
                    try:
                        cabina = self._crea_oggetto_cabina(riga)
                        self.cabine[cabina.codice] = cabina
                    except Exception as e:
                        print(f"Attenzione: Impossibile creare la cabina dalla riga {riga}. Errore: {e}")

                elif codice.startswith('P'):
                    # Riga relativa a un Passeggero (codice, nome, cognome)
                    if len(riga) >= 3:
                        passeggero = Passeggero(codice, riga[1], riga[2])
                        self.passeggeri[passeggero.codice] = passeggero
                    else:
                        print(f"Attenzione: Dati passeggero incompleti nella riga {riga}.")

    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        # 1. Verifica esistenza cabina
        if codice_cabina not in self.cabine:
            raise ValueError(f"Errore: Cabina con codice '{codice_cabina}' non trovata.")

        cabina = self.cabine[codice_cabina]

        # 2. Verifica esistenza passeggero
        if codice_passeggero not in self.passeggeri:
            raise ValueError(f"Errore: Passeggero con codice '{codice_passeggero}' non trovato.")

        passeggero = self.passeggeri[codice_passeggero]

        # 3. Verifica disponibilità cabina
        if not cabina.disponibile:
            raise ValueError(f"Errore: Cabina {codice_cabina} non disponibile (già occupata).")

        # 4. Verifica se il passeggero ha già una cabina
        if passeggero.cabina_assegnata is not None:
            raise ValueError(
                f"Errore: Passeggero {codice_passeggero} ha già una cabina assegnata ({passeggero.cabina_assegnata.codice}).")

        # Assegnazione
        cabina.disponibile = False
        passeggero.cabina_assegnata = cabina
        self.prenotazioni[codice_passeggero] = codice_cabina

        print(f"Successo: Cabina {codice_cabina} assegnata a {passeggero.nome} {passeggero.cognome}.")
        return True

    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        # Sfrutta il metodo dunder __lt__ implementato nella classe Cabina
        lista_cabine = list(self.cabine.values())
        return sorted(lista_cabine)


    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        print("\n--- ELENCO PASSEGGERI E PRENOTAZIONI ---")
        if not self.passeggeri:
            print("Nessun passeggero caricato.")
            return

        for passeggero in self.passeggeri.values():
            info_passeggero = f"{passeggero.codice} - {passeggero.nome} {passeggero.cognome}"

            if passeggero.cabina_assegnata:
                info_cabina = f" | Cabina: {passeggero.cabina_assegnata.codice} ({passeggero.cabina_assegnata.tipo}) - Prezzo: {passeggero.cabina_assegnata.get_prezzo_finale():.2f}€"
            else:
                info_cabina = " | NESSUNA CABINA ASSEGNATA"

            print(info_passeggero + info_cabina)
        print("---------------------------------------")



