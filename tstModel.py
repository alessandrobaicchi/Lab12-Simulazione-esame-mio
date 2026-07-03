from model.model import Model

mymodel = Model()
mymodel.getBuiltGraph(7.4, 7.8)
nodi, archi = mymodel.getGraphDetails()
top5edges = mymodel.getBest5edges()
numComponents, maxComponent, lunLargestComponent = mymodel.getConnectedComponents()
print(f"Grafo creato! Il grafo contiente {nodi} nodi e {archi} archi.")
print("A seguire i 5 migliori archi del grafo:")
for n in top5edges:
    print(f"{n[0]} --> {n[1]}: {n[2]["weight"]}")
print(f"Il grafo contiene {numComponents} componenti connesse.")
print(f"La componente connessa più grande è lunga {lunLargestComponent}:")
for a in maxComponent:
    print(a)


