from model.model import Model

mymodel = Model()
mymodel.getBuiltGraph(1.2, 2.7)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato! Il grafo contiente {nodi} nodi e {archi}.")

