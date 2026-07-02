import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ratingMinValue = None
        self._ratingMaxValue = None

    # ----------------------------------------- DDs "Voti" ---------------------------------------------
    def fillDDsRating(self):
        voti = self._model.getVoti()
        votiDD1 = list(map(lambda x: ft.dropdown.Option(x, on_click=self._choiceRating1), voti))
        votiDD2 = list(map(lambda x: ft.dropdown.Option(x, on_click=self._choiceRating2), voti))

        self._view._ddrating1.options = votiDD1
        self._view._ddrating2.options = votiDD2
        self._view.update_page()


    def _choiceRating1(self,e):
        self._ratingMinValue = e.control.data

    def _choiceRating2(self,e):
        self._ratingMaxValue = e.control.data

    # --------------------------------------------------------------------------------------------------

    def handleCreaGrafo(self, e):
        pass

    def handleCammino(self, e):
        pass