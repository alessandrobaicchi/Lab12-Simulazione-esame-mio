from model.model import Model

mymodel = Model()
mymodel.getBuiltGraph(7.4, 7.8)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato! Il grafo contiente {nodi} nodi e {archi}.")

