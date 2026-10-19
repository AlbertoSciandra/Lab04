class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.__codice=codice
        self.__superficie=float(superficie)
        self.__padiglione=int(padiglione)
        self.__prezzo_base=float(prezzo_base)
        self.__disponibile = True
        self.__espositore = None
    def calcola_prezzo(self):
        return self.prezzo_base

    @property
    def codice(self):
        return self.__codice

    @property
    def espositore(self):
        return self.__espositore

    @espositore.setter
    def espositore(self, nuovo_espositore):
        self.__espositore = nuovo_espositore

    @property
    def disponibile(self):
        return self.__disponibile

    @disponibile.setter
    def disponibile(self, nuovo_disponibile):
        self.__disponibile = nuovo_disponibile

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

class StandStandard(Stand):
    def __str__(self):
        if self.disponibile:
            stato="disponibile"
        else:
            stato = f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"

class StandPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base,numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        if self.disponibile:
            stato="disponibile"
        else:
            stato = f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.poszione= posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30


    def __str__(self):
        if self.disponibile:
            stato="disponibile"
        else:
            stato = f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Stand Premium | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        stand_str = f"Stand: {self.stand.codice}" if self.stand else "Nessuno stand associato"
        return f"{self.codice}: {self.nome} {self.cognome} - {stand_str}"


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self.__nome = nome
        self.__stand = []
        self.__espositori = []

        @property
        def nome(self):
            return self.__nome

        @nome.setter
        def nome(self, nuovo_nome):
            if not nuovo_nome or not isinstance(nuovo_nome, str):
                raise ValueError("Il nome deve essere una stringa non vuota")
            self.__nome = nuovo_nome

    def carica_file_dati(self, file_path):
        try:
            file = open(file_path, "r", encoding="utf-8")
            for riga in file:
                riga = riga.strip()
                campi = [c.strip() for c in riga.split(",")]

                codice = campi[0]
                if codice.startswith("ST"):
                    dati_stand = [c for c in campi if c != "<unset>"]
                    lunghezza = len(dati_stand)
                    if lunghezza == 4:
                        codice = dati_stand[0]
                        misura = dati_stand[1]
                        padiglione = dati_stand[2]
                        prezzo = dati_stand[3]

                        nuovo_stand = StandStandard(codice, misura, padiglione, prezzo)
                        self.__stand.append(nuovo_stand)
                    elif lunghezza == 5:
                        ultimo_campo = dati_stand[4]

                        if ultimo_campo.isdigit():
                            codice = dati_stand[0]
                            misura = dati_stand[1]
                            padiglione = dati_stand[2]
                            prezzo = dati_stand[3]
                            prese = dati_stand[4]
                            nuovo_stand = StandPrese(codice, misura, padiglione, prezzo, prese)
                            self.__stand.append(nuovo_stand)
                        else:
                            codice = dati_stand[0]
                            misura = dati_stand[1]
                            padiglione = dati_stand[2]
                            prezzo = dati_stand[3]
                            posizione = dati_stand[4]
                            nuovo_stand = StandPremium(codice, misura, padiglione, prezzo, posizione)
                            self.__stand.append(nuovo_stand)
                elif codice.startswith("ES"):
                    dati_espositore = [c for c in campi if c != "<unset>"]
                    if len(dati_espositore) >= 3:
                        codice = dati_espositore[0]
                        nome = dati_espositore[1]
                        cognome = dati_espositore[2]
                        nuovo_espositore = Espositore(codice, nome, cognome)
                        self.__espositori.append(nuovo_espositore)
            file.close()
        except FileNotFoundError:
            print("Il file non esiste")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        stand_trovato = None
        espositore_trovato = None

        for s in self.__stand:
            if s.codice == codice_stand:
                stand_trovato = s
                break

        for e in self.__espositori:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        if not stand_trovato:
            raise ValueError(f"lo stand non esiste")
        if not espositore_trovato:
            raise ValueError(f"l'espositore non esiste")

        for s in self.__stand:
            if s.espositore == espositore_trovato:
                raise ValueError(f"all'espositore è già stato sassegnato lo stand {s.codice}")

        stand_trovato.espositore = espositore_trovato
        print(f"assegnazione completata")

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO
        for e in self.__espositori:
            stand_associato = None

        for s in self.__stand:
            if s.espositore == e:
                stand_associato = s.codice
                break
        if stand_associato:
            print(f"Espositore: {e.codice}, {e.nome}, {e.cognome} - stand associato: {stand_associato}")
        else:
            print(f"Espositore: {e.codice}, {e.nome}, {e.cognome} - nessuno stand associato")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO
        stand_ordinati = sorted(self.__stand)
        return stand_ordinati
