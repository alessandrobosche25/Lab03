import csv
from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"{self.codice} - {self.tipo} {self.marca} (Acquistato: {self.anno_acquisto}, Valore: {self.valore}€)"

class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.codice}: Strumento {self.id_strumento} a {self.cognome_allievo} (in data {self.data})"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self._responsabile = responsabile
        
        self.strumenti = {} 
        self.prestiti = []
        
        self.contatore_strumenti = 0
        self.contatore_prestiti = 0

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                lettore_csv = csv.reader(file)
                for riga in lettore_csv:
                    if not riga or riga[0] == 'codice': 
                        continue
                    
                    codice, tipo, marca, anno_acquisto, valore = riga
                    
                    nuovo_strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
                    self.strumenti[codice] = nuovo_strumento
                    
                    numero_codice = int(codice[1:])
                    if numero_codice > self.contatore_strumenti:
                        self.contatore_strumenti = numero_codice
            print(f"Caricati {len(self.strumenti)} strumenti dal file.")

        except FileNotFoundError:
            raise FileNotFoundError(f"Il file '{file_path}' non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self.contatore_strumenti += 1
        nuovo_codice = f"S{self.contatore_strumenti}"
        
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = nuovo_strumento
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self.strumenti.values())
        lista_strumenti.sort(key=attrgetter('marca'))
        return lista_strumenti

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: lo strumento con codice {id_strumento} non esiste nel deposito.")

        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception(f"Errore: lo strumento {id_strumento} è già attualmente in prestito.")

        self.contatore_prestiti += 1
        codice_prestito = f"P{self.contatore_prestiti}"
        
        nuovo_prestito = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(nuovo_prestito)
        
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        prestito_da_rimuovere = None
        for p in self.prestiti:
            if p.codice == id_prestito:
                prestito_da_rimuovere = p
                break
                
        if prestito_da_rimuovere:
            self.prestiti.remove(prestito_da_rimuovere)
            return True
        else:
            raise Exception(f"Errore: nessun prestito attivo trovato con il codice '{id_prestito}'.")