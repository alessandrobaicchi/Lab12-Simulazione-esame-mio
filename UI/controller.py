import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # ----------------------------------------- DDs "Voti" ---------------------------------------------
    def fillDDsRating(self):
        voti = self._model.getVoti()

        for voto in voti:
            self._view._ddrating1.options.append(ft.dropdown.Option(voto))
            self._view._ddrating2.options.append(ft.dropdown.Option(voto))

        self._view.update_page()

    # --------------------------------------------------------------------------------------------------

    # ---------------------------------------- Tasto "Crea Grafo" --------------------------------------
    def handleCreaGrafo(self, e):
        self._model.getBuiltGraph(self._view._ddrating1.value, self._view._ddrating2.value)

        self._view.txt_result.controls.clear()
        numNodi, numArchi = self._model.getGraphDetails()
        top5edges = self._model.getBest5edges()
        numComponents, maxComponent, lunLargestComponent = self._model.getConnectedComponents()

        self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {numNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {numArchi}"))

        self._view.txt_result.controls.append(ft.Text("A seguire i top 5 archi:"))
        for u, v, data in top5edges:
            self._view.txt_result.controls.append(ft.Text(f"{u.name} --> {v.name}: {data['weight']}"))

        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {numComponents} componenti connesse."))
        self._view.txt_result.controls.append(ft.Text(
                                            f"La componente connessa più grande è lunga: {lunLargestComponent}"))
        for a in maxComponent:
            self._view.txt_result.controls.append(ft.Text(a))

        self._view.update_page()

    # --------------------------------------------------------------------------------------------------

    def handleCammino(self, e):
        pass