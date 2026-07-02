import networkx as nx

from database import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._actors = []
        self._idMapActors = {}

    # -------------------------------------- DDs "Voti" ----------------------------------------------
    def getVoti(self):
        return DAO.getVoti()
    # ------------------------------------------------------------------------------------------------

    # -------------------------------------- Crea grafo ----------------------------------------------
    def getBuiltGraph(self, startRange, endRange):
        self._grafo.clear()

        # Nodi
        self._actors = DAO.getNodes(startRange, endRange)
        self._grafo.add_nodes_from(self._actors)
        self._idMapActors = {a.id: a for a in self._actors}

        # Archi
        edgesGross = DAO.getEdges()     # Sono potenziali archi

        # Dizionario per sommare gli incassi dei film in comune
        edgesSum = {}

        # Accesso alle tuple di edgesGross in modo "Pythonico"
        for actor1, actor2, income in edgesGross:
            # Verifico che entrambi gli attori siano attori validi (cioè che siano nodi del grafo)
            if actor1 in self._idMapActors and actor2 in self._idMapActors:
                # "Ripulisco" l'incasso del film che hanno in comune (income delle tuple di edgeGross)"
                incasso = self._cleanIncome(income)

                # Somma degli incassi per la coppia
                edgesSum[(actor1, actor2)] = edgesSum.get((actor1, actor2), 0) + incasso

        # Aggiungo gli archi al grafo
        for (actor1, actor2), peso in edgesSum.items():
            self._grafo.add_edge(self._idMapActors[actor1], self._idMapActors[actor2], weight=peso)


    def _cleanIncome(self, income):
        if income is None:
            return 0

        # Converto in stringa
        s = str(income)

        # Rimuovo simboli di valuta e spazi
        for ch in ["USD", "$", "€", " ", ","]:
            s = s.replace(ch, "")

        # Se dopo la pulizia non è un numero -> ritorna 0
        if not s.isdigit():
            return 0

        return int(s)


    def getGraphDetails(self):
        return (len(self._grafo.nodes), len(self._grafo.edges))
    # ------------------------------------------------------------------------------------------------