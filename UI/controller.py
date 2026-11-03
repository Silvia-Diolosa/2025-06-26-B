import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        years = self._model.getAllYear()
        for year in years:
            self._view._ddYear1.options.append(ft.dropdown.Option(year))
            self._view._ddYear2.options.append(ft.dropdown.Option(year))

        self._view.update_page()

    def handleBuildGraph(self, e):
        if self._view._ddYear1 is None or self._view._ddYear2 is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un valore dal menu."))
            return

        self._model.buildGraph(self._view._ddYear1.value, self._view._ddYear2.value)
        nNodi, nArchi = self._model.getGraphDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="green"))
        self._view._txt_result.controls.append(
            ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))
        self._view.update_page()


    def handlePrintDetails(self, e):
        self._view._txt_result.controls.clear()
        largest = self._model.getCompConn()
        for tupla in largest:
            self._view._txt_result.controls.append(ft.Text(f"{tupla[0]}-- {tupla[1]}"))

        self._view.update_page()




    def handleCercaDreamChampionship(self, e):
        pass

