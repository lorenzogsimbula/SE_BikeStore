import copy

import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.G = nx.DiGraph()
        self._idMap = {}
        self.soluzione_best=[]
        self.peso_best=0


    def get_date_range(self):
        return DAO.get_date_range()

    def get_category(self):
        return DAO.get_category()


    def get_product(self,cat):
        return DAO.get_product(cat)



    def build_graph(self,categoria,data1,data2):
        self.G.clear()

        self._nodes=DAO.get_product(categoria)
        self.G.add_nodes_from(self._nodes)
        for node in self._nodes:
            self._idMap[node.id] = node

        vendite_diz=DAO.get_product_vendite(categoria,data1,data2)

        prodotti_venduti=[]

        for id , dati in vendite_diz.items():
            if id in self._idMap:
                prod_ogg=self._idMap[id]
                prod_ogg.vendite=dati
                prodotti_venduti.append(prod_ogg)
        for i in range(len(prodotti_venduti)):
            for j in range(len(prodotti_venduti)):
                if i==j:
                    continue

                n1=prodotti_venduti[i]
                n2=prodotti_venduti[j]

                peso_totale=n1.vendite+n2.vendite
                if n1.vendite>n2.vendite:
                    self.G.add_edge(n1,n2,weight=peso_totale)
                elif n1.vendite<n2.vendite:
                    self.G.add_edge(n2,n1,weight=peso_totale)
                else:
                    self.G.add_edge(n1,n2,weight=peso_totale)
                    self.G.add_edge(n2,n1,weight=peso_totale)



        return self.G

    def get_best_products(self):

        result=[]

        for n in self.G.nodes:
            peso_uscenti=sum([self.G[u][v]['weight'] for u,v in self.G.out_edges(n)])
            peso_entranti=sum([self.G[u][v]['weight'] for u,v in self.G.in_edges(n)])

            diff=peso_uscenti-peso_entranti
            result.append((n,diff))

        result.sort(key=lambda x:x[1],reverse=True)

        return result[:5]
    def trova_cammino(self,lung,start,end):
        self.soluzione_best=[]
        self.peso_best=0

        parziale=[start]

        self.ricorsione(parziale,lung,end)

        return self.soluzione_best, self.peso_best


    def ricorsione(self,parziale,lung,end):

        if len(parziale)==lung:
            if parziale[-1]==end and self.get_score(parziale)>self.peso_best:
                self.peso_best=self.get_score(parziale)
                self.soluzione_best=copy.deepcopy(parziale)
                return
        if len(parziale)>lung:
            return
        for n in self.G.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale,lung,end)
                parziale.pop()




    def get_score(self, parziale):
        score = 0
        for i in range(1, len(parziale)):
            score += self.G[parziale[i-1]][parziale[i]]["weight"]
        return score












