from model.model import Model

mymodel = Model()
mymodel.getBuiltGraph(7.4, 7.8)
# nodi, archi = mymodel.getGraphDetails()
# top5edges = mymodel.getBest5edges()
# numComponents, maxComponent, lunLargestComponent = mymodel.getConnectedComponents()
# print(f"Grafo creato! Il grafo contiente {nodi} nodi e {archi} archi.")
# print("A seguire i 5 migliori archi del grafo:")
# for n in top5edges:
#     print(f"{n[0]} --> {n[1]}: {n[2]["weight"]}")
# print(f"Il grafo contiene {numComponents} componenti connesse.")
# print(f"La componente connessa più grande è lunga {lunLargestComponent}:")
# for a in maxComponent:
#     print(a)

actors = list(mymodel._grafo.nodes())
# ----------------------------------------------------------------------------------
# source = next(a for a in actors if a.name == "Robert Downey Jr.")
# target = next(a for a in actors if a.name == "Chris Evans")
# Se voglio selezionare un attore specifico dal grafo, posso usare:
#
#     source = next(a for a in actors if a.name == "Robert Downey Jr.")
#
# Significato:
#   - 'actors' è la lista dei nodi del grafo (oggetti Actor)
#   - 'a for a in actors if a.name == ...' è un generatore che produce
#     tutti gli attori il cui nome corrisponde alla stringa indicata.
#   - 'next(...)' prende il PRIMO attore che soddisfa la condizione.
# ----------------------------------------------------------------------------------
source = actors[0]
target = actors[1]
allPath = mymodel.getAllPath(source, target)
print(f"A seguire tutti i cammini semplici a partire da {source} a {target}")
for cammino in allPath:
    print(" -> ".join(a.name for a in cammino))

# ========================= APPUNTI: stampa dei cammini con .join() =========================
#
# Quando ho una lista di cammini (allPath), ogni cammino è una lista di Actor.
# Esempio:
#     cammino = [Actor("Alan Bates"), Actor("Marie Matiko"), Actor("Monica Calhoun")]
#
# Voglio stampare ogni cammino su UNA sola riga, mostrando SOLO i nomi degli attori,
# separati da " -> ".
#
# La sintassi:
#
#     " -> ".join(a.name for a in cammino)
#
# funziona così:
#
#   1) (a.name for a in cammino)
#      È un GENERATORE: per ogni attore 'a' dentro la lista 'cammino',
#      produce la stringa a.name.
#      Esempio: "Alan Bates", "Marie Matiko", "Monica Calhoun"
#
#   2) " -> ".join(...)
#      join() prende tutte le stringhe prodotte dal generatore e le unisce
#      usando " -> " come separatore.
#
#      Risultato finale:
#          Alan Bates -> Marie Matiko -> Monica Calhoun
#
#   3) La stampa completa:
#
#     for cammino in allPath:
#         print(" -> ".join(a.name for a in cammino))
#
#      Stampa ogni cammino su una riga, in modo pulito e leggibile.
#
# Versione numerata (più elegante):
#
#     for i, cammino in enumerate(allPath, start=1):
#         print(f"Cammino {i}: " + " -> ".join(a.name for a in cammino))
#
# ===========================================================================================
