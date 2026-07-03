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