import copy

import networkx as nx

from database import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._actors = []
        self._edges = []
        self._idMapActors = {}

    # ------------------------------------------- DDs "Voti" ------------------------------------------------
    def getVoti(self):
        return DAO.getVoti()
    # -------------------------------------------------------------------------------------------------------

    # =========================================== Crea grafo ================================================
    def getBuiltGraph(self, startRange, endRange):
        self._grafo.clear()

        # Nodi
        self._actors = DAO.getNodes(startRange, endRange)
        self._grafo.add_nodes_from(self._actors)
        self._idMapActors = {a.id: a for a in self._actors}

        # Archi
        self._edges = DAO.getEdges(startRange, endRange)

        # Aggiungo gli archi al grafo
        for actor1, actor2, peso in self._edges:
            self._grafo.add_edge(self._idMapActors[actor1], self._idMapActors[actor2], weight=peso)


    # ----------------------------------------------------------------------------
    # Metodo non più usato in questa applicazione, ma utile da avere sottomano
    # def _cleanIncome(self, income):
    #     if income is None:
    #         return 0
    #
    #     # Converto in stringa
    #     s = str(income)
    #
    #     # Rimuovo simboli di valuta e spazi
    #     for ch in ["USD", "$", "€", " ", ","]:
    #         s = s.replace(ch, "")
    #
    #     # Se dopo la pulizia non è un numero -> ritorna 0
    #     if not s.isdigit():
    #         return 0
    #
    #     return int(s)
    # -----------------------------------------------------------------------------------------------------

    def getGraphDetails(self):
        return (len(self._grafo.nodes), len(self._grafo.edges))


    def getBest5edges(self):
        edges = self._grafo.edges(data=True)
        # E' una lista del tipo (actorObj1, actorObj2, {"weight: 123456"}
        edgesSorted = sorted(edges, key=lambda x: x[2]["weight"], reverse=True)
        return edgesSorted[:5]


    def getConnectedComponents(self):
        components = list(nx.connected_components(self._grafo))
        # E' una lista che contiene le varie componenti connesse del tipo:
        # [
        #     {ActorObj1, ActorObj7, ActorObj9},
        #     {ActorObj3, ActorObj4},
        #     {ActorObj10},
        #     ...
        # ]

        # Calcolo il numero di componenti connesse del grafo
        numComponents = len(components)

        # Trovo la componente più grande
        largestComponent = max(components, key=len)
        lunLargestComponent = len(largestComponent)
        return numComponents, largestComponent, lunLargestComponent
    # ======================================================================================================


    # ========================================== Ricorsione ================================================
    '''Uso una visita ricorsiva DFS sul grafo degli attori.'''

    def getBestPath(self):
        self._bestPath = []

        for actorStart in self._grafo.nodes():
            parziale = [actorStart]
            self._ricorsione(parziale)

        return self._bestPath


    def _ricorsione(self, parziale):
        # 1) Condizione di ottimalità
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        actorCorrente = parziale[-1]

        # 2) Condizione di terminazione, qui non serve perché la terminazione è garantita dal cammino semplice
        #    dato dall'età decrescente: quando non ci sono vicini validi la ricorsione si ferma da sola!

        # 3) Ricorsione
        for vicino in self._grafo.neighbors(actorCorrente):
            if vicino not in parziale and vicino.date_of_birth < actorCorrente.date_of_birth:
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()


    # ======================================================================================================

    # ================================ Ricorsione extra - per esercitarmi ==================================
    def getAllPath(self, source, target):
        self._allCammini = []
        parziale = [source]
        self._ricorsioneAllCammini(parziale, target)
        return self._allCammini


    def _ricorsioneAllCammini(self, parziale, target):
        actCorrente = parziale[-1]
        # Condizione di ottimalità
        if actCorrente == target:
            self._allCammini.append(list(parziale))
            return

        # Condizione ricorsiva
        for vicino in self._grafo.neighbors(actCorrente):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsioneAllCammini(parziale, target)
                parziale.pop()

    # ========================= APPUNTI: Ricorsione getAllPath =========================
    #
    # Obiettivo:
    #     Trovare TUTTI i cammini semplici da un nodo 'source' a un nodo 'target'
    #     nel grafo degli attori.
    #
    # DEFINIZIONI:
    # - Cammino semplice: nessun nodo ripetuto.
    # - Ricorsione DFS: esploro i vicini del nodo corrente, espando il cammino,
    #   e poi torno indietro (backtracking).
    #
    # -----------------------------------------------------------------------------------
    # FUNZIONE PUBBLICA: getAllPath(source, target)
    #
    #     self._allCammini = []
    #         Inizializzo la lista che conterrà TUTTI i cammini trovati.
    #
    #     parziale = [source]
    #         Il cammino parziale parte dal nodo sorgente.
    #
    #     self._ricorsioneAllCammini(parziale, target)
    #         Avvio la ricorsione.
    #
    #     return self._allCammini
    #         Ritorno la lista di tutti i cammini trovati.
    #
    # -----------------------------------------------------------------------------------
    # FUNZIONE RICORSIVA: _ricorsioneAllCammini(parziale, target)
    #
    #     actCorrente = parziale[-1]
    #         Il nodo corrente è l'ultimo del cammino parziale.
    #
    # ------------------------- CASO BASE -----------------------------------------------
    #
    #     if actCorrente == target:
    #         self._allCammini.append(list(parziale))
    #         return
    #
    # Significato:
    #   - Ho raggiunto il nodo target → il cammino è completo.
    #   - Aggiungo una COPIA del cammino alla lista dei cammini.
    #   - return → mi fermo: non devo espandere oltre il target.
    #
    # ------------------------- CASO RICORSIVO ------------------------------------------
    #
    #     for vicino in self._grafo.neighbors(actCorrente):
    #         if vicino not in parziale:
    #             parziale.append(vicino)
    #             self._ricorsioneAllCammini(parziale, target)
    #             parziale.pop()
    #
    # Significato:
    #   - Scorro tutti i vicini del nodo corrente.
    #   - Se il vicino NON è già nel cammino → mantengo il cammino semplice.
    #   - Aggiungo il vicino al cammino (espansione).
    #   - Chiamo ricorsivamente la funzione per continuare l'esplorazione.
    #   - Dopo la ricorsione → parziale.pop() (BACKTRACKING):
    #         torno indietro allo stato precedente del cammino.
    #
    # -----------------------------------------------------------------------------------
    # MECCANICA DELLA DFS CON CAMMINO SEMPLICE:
    #
    #   1) Espando il cammino aggiungendo un vicino.
    #   2) Ricorro.
    #   3) Quando la ricorsione torna indietro → rimuovo l'ultimo nodo.
    #   4) Provo un altro vicino.
    #   5) Ripeto finché non ho esplorato tutte le possibilità.
    #
    # Questo schema garantisce:
    #   - Nessun ciclo (grazie a "vicino not in parziale")
    #   - Esplorazione completa di tutti i cammini possibili
    #   - Nessuna condizione di terminazione esplicita oltre al caso base
    #
    # -----------------------------------------------------------------------------------
    # ESEMPIO DI STAMPA DEI CAMMINI:
    #
    #     for cammino in allPath:
    #         print(" -> ".join(a.name for a in cammino))
    #
    # Spiegazione:
    #   - a.name for a in cammino → prendo il nome di ogni attore nel cammino.
    #   - " -> ".join(...) → unisco i nomi con " -> " come separatore.
    #   - Risultato: stampa pulita del cammino su una sola riga.
    #
    # ===================================================================================

    # ======================================================================================================