from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO

        if self.dd_category_value is None:
            self._view.show_alert("inserisci categoria")
        if self._view.dp1.value is None:
            self._view.show_alert("inserisci data inzio")
        if self._view.dp2.value is None:
            self._view.show_alert("inserisci data fine")
        grafo=self._model.build_graph(self.dd_category_value,self._view.dp1.value,self._view.dp2.value)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {self._view.dp1.value.date()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {self._view.dp2.value.date()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {grafo.number_of_nodes()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {grafo.number_of_edges()}"))
        self._populate_dd_products()
        self._view.page.update()




    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO

        risultati=self._model.get_best_products()
        self._view.txt_risultato.controls.append(ft.Text(f"I cinque prodotti più venduti sono:"))
        for r, diff in risultati:
            self._view.txt_risultato.controls.append(ft.Text(f"{r} with score {diff}"))

        self._view.page.update()


    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """

        # TODO
        try:
            lung= int(self._view.txt_lunghezza_cammino.value)
        except (ValueError, TypeError):
            self._view.show_alert("Inserisci un valore numerico intero per la lunghezza.")
            return
        if self._view.txt_lunghezza_cammino.value is None:
            self._view.show_alert("inserisci lunghezza cammino")
        if self.dd_prod_start_value is None:
            self._view.show_alert('seleziona prodotto iniziale')
        if self.dd_prod_end_value is None:
            self._view.show_alert('seleziona prodotto finale')
        cammino,score=self._model.trova_cammino(lung,self.dd_prod_start_value,self.dd_prod_end_value)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Cammino migliore:"))

        for c in cammino:
            self._view.txt_risultato.controls.append(ft.Text(f"{c}"))

        self._view.txt_risultato.controls.append(ft.Text(f"Score: {score}"))
        self._view.page.update()



    def popola_category(self):
        categories=self._model.get_category()

        self._view.dd_category.options=[ft.dropdown.Option(key=c.category_name, data=c) for c in categories]

        self._view.page.update()

    def choice_category(self, e):

        selected_key = e.control.value

        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_category_value = opt.data
                break
    def _populate_dd_products(self):
        all_nodes = self._model._nodes
        self._view.dd_prodotto_iniziale.options = [ft.dropdown.Option(key=c.product_name, data=c) for c in all_nodes]
        self._view.dd_prodotto_finale.options = [ft.dropdown.Option(key=c.product_name, data=c) for c in all_nodes]
        self._view.update()
    def choice_prod_start(self, e):

        selected_key = e.control.value

        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_prod_start_value = opt.data
                break

    def choice_prod_end(self, e):

        selected_key = e.control.value

        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_prod_end_value  = opt.data
                break