import xlrd, var, events, conexion
from PyQt5 import QtWidgets

from xlrd import open_workbook


class Importar():
    def importarDatos(self):
        """

        Modulo que importa los datos de productos de un archivo .xls y se agregan a la base de datos o si existen se actualiza el precio y stock.

        :return: None
        :rtype: None

        """
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgabrir.getOpenFileName(None, 'Importar Productos', '', '*.xls',
                                                        options=option)
            mensaje = 'Desea importar ese archivo?'
            var.validar = False
            if var.filedlgabrir.Accepted and filename[0] != '':
                events.Eventos.AbrirAviso(mensaje)
                if var.validar == True:

                    documento = xlrd.open_workbook(str(filename[0]))

                    frutas = documento.sheet_by_index(0)
                    fila = frutas.nrows
                    col = frutas.ncols
                    for i in range(1, fila):
                        producto = []
                        for j in range(col):
                            producto.append(frutas.cell_value(i, j))
                        producto[1] = str(producto[1])
                        fruta = conexion.Conexion.productoExistente(producto[0])
                        if fruta is None:
                            conexion.Conexion.altaPro(producto)

                        else:
                            stock1 = int(producto[2])
                            stock2 = int(fruta[3])

                            producto[2] = stock1 + stock2
                            conexion.Conexion.modifProducto(fruta[0], producto)
                            conexion.Conexion.mostrarProductos()
                    conexion.Conexion.mostrarProductos()
                    var.ui.lblstatus.setText('Productos importados')

        except Exception as error:
            print('Error importar datos ' % str(error))
