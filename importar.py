import xlrd

class Importar():
    def importarDatos(self):
        documento = xlrd.open_workbook("")
        frutas = documento.sheet_by_index(0)

