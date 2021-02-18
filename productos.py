import var
from PyQt5 import QtWidgets
import conexion, events

class Productos():

    def AltaProductos(self):

        try:
            newpro = [] #contiene todos los datos
            producto = [var.ui.editNombrePro,var.ui.editPrecioPro,var.ui.editStock]
            for i in producto:
                newpro.append(i.text())
            mensaje = ('Desea dar de alta el Producto?')
            events.Eventos.AbrirAviso(mensaje)
            if var.validar==True:
                if newpro:
                    conexion.Conexion.altaPro(newpro)
                    Productos.limpiarPro(self)


        except Exception as error:
            print('Error alta Productos: %s ' % str(error))

    def cargarPro(self):
        try:
            fila = var.ui.tablaPro.selectedItems()
            producto = [var.ui.lblCodigoPro, var.ui.editNombrePro, var.ui.editPrecioPro]
            if fila:
                fila = [dato.text() for dato in fila]  # coge los datos de una fila de la tablaCli
            for i, dato in enumerate(producto):
                dato.setText(fila[i])  # Introduce los datos de fila en los editText de client
            conexion.Conexion.cargarProducto(self)


        except Exception as error:
            print('Error cargar Productos: %s ' % str(error))



    def bajaProducto(self):
        try:
            var.validar=False
            codigo=var.ui.lblCodigoPro.text()
            mensaje=('Desea eliminar el Producto?')

            if var.ui.lblCodigoPro.text()!='':
                events.Eventos.AbrirAviso(mensaje)
            if var.validar==True:
                conexion.Conexion.bajaPro(codigo)
                conexion.Conexion.mostrarProductos()
                Productos.limpiarPro(self)

        except Exception as error:
            print('Error bajar Productos: %s' %str(error))

    def modifProducto(self):

        try:
            var.validar=False
            newdata=[]
            codigo=var.ui.lblCodigoPro.text()
            producto=[var.ui.editNombrePro, var.ui.editPrecioPro,var.ui.editStock]
            for i in producto:
                newdata.append(i.text())
            mensaje=('Seguro que desea Modificar el Producto?')
            events.Eventos.AbrirAviso(mensaje)
            if var.validar==True:
                conexion.Conexion.modifProducto(codigo,newdata)
                conexion.Conexion.mostrarProductos()
                Productos.limpiarPro(self)
        except Exception as error:
            print('Error modifProducto: %s' %str(error))
    def limpiarPro(self):

        try:
            var.ui.lblCodigoPro.setText('')
            var.ui.editNombrePro.setText('')
            var.ui.editPrecioPro.setText('')
            var.ui.editStock.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))