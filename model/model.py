import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.idMap = {}



    def getAllYear(self):
        return DAO.getAllYears()


    def buildGraph(self, anno1, anno2):
        self._graph.clear()
        self.idMap.clear()


        nodes = DAO.getAllNodes()
        for node in nodes:
            self.idMap[node.circuitId] = node

        self._graph.add_nodes_from(nodes)

        self.aggiungiDiz(anno1, anno2)

        edges = DAO.getAllEdges(anno1, anno2)
        for edge in edges:
            u = self.idMap[edge[0]]
            v = self.idMap[edge[1]]
            peso = self.calcolaPeso(u,v)
            self._graph.add_edge(u, v, weight=peso)


    def calcolaPeso(self, u, v):
        pesoU = 0
        for chiave, valore in u.diz.items():
            for (driver, tempo) in valore:
                if tempo is not None:
                    pesoU += 1
        pesoV = 0
        for chiave, valore in v.diz.items():
            for (driver, tempo) in valore:
                if tempo is not None:
                    pesoV += 1

        return pesoU + pesoV

    def aggiungiDiz(self, anno1, anno2):
        result = DAO.getDiz(anno1, anno2)
        for r in result:
            circuito = self.idMap[r[0]]
            dizionario = circuito.diz
            if r[1] not in dizionario:
                dizionario[r[1]] = []
            dizionario[r[1]].append((r[2], r[3]))



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getCompConn(self):
        # Un grafo può essere formato da più “isole” di nodi collegati tra loro.
        # Ogni isola è una componente connessa. Qui ce n’è una grande e poi, tra le altre, i circuiti isolati
        # (le componenti da un solo nodo). Devi prendere l’isola con più nodi e lavorare solo su quella:
        # max(components, key=len).
        #
        # 2. Come ordinare i suoi nodi
        #
        # Ogni nodo ha uno o più archi, e ogni arco ha un peso. Per ogni nodo guardi i pesi dei suoi archi
        # e prendi il più piccolo. Quel numero è il “peso minimo degli archi incidenti” (incidenti = che toccano
        # quel nodo). Poi ordini i nodi dal valore più alto al più basso.

        components = list(nx.connected_components(self._graph))
        # largest = list(max(components, key=len))
        largest = components[0]

        lista = []

        for nodo in largest:
            pesi = []
            archi = self._graph.edges(nodo, data=True)
            for arco in archi:
                pesi.append(arco[2]['weight'])

            pesoMin = min(pesi)

            lista.append((nodo, pesoMin))

            lista.sort(key=lambda x: x[1], reverse=True)



        return lista


