import os
import sys

from PyQt5 import QtWidgets, QtSql, QtCore
import var, ventas


class Conexion():

    def db_connect(filename):
        """

        Módulo que realiza la conexion de la aplicacion con la bd

        :param filename: nombre de la base de datos
        :type filename: string
        :return: bool
        :rtype: True/False

        Utiliza la libreria de QtSql y el gestor de la BBDD es SqLite. En caso de error muestra pantalla de aviso

        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(Conexion.resource_path(filename))
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n' 'Haz Click para Cancelar.',
                                           QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
            return True

    def resource_path(relative_path):
        """

        Obtiene el directorio de los recursos para hacer el onefile

        :param a: Ruta del archivo que queremos localizar
        :type a: String
        :return: Ruta del recurso
        :rtype: String

        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def altaCli(cliente):
        """

        Módulo que da de alta un cliente con los datos pasados por lista. Muestra mensaje de resultado en la statusbar.
        Rescarga la tablaCli

        :param cliente: datos del cliente
        :type cliente: lista
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago, edad)'
            'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', str(cliente[8]))
        if query.exec_():
            print("Inserción Correcta")
            Conexion.mostrarClientes(False)
            var.ui.lblstatus.setText('Inserción correcta')
        else:
            print("Error: ", query.lastError().text())

    def mostrarClientes(op):
        """

        Carga los clientes de la base de datos en la tablaCli

        :param a: Boolean para realizar la busqueda de un cliente concreto o no
        :type a: Boolean
        :return: None
        :rtype: None

        """
        index = 0
        var.ui.spinEdad.setValue(16)
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        if op == True:
            query.prepare('select dni, apellidos, nombre from clientes where dni=:dni;')
            query.bindValue(':dni', dni)
        else:
            query.prepare('select dni, apellidos, nombre from clientes;')

        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)  # coge los valores de la consulta y se guardan en estas variables
                nombre = query.value(2)
                var.ui.tablaCli.setRowCount(index + 1)  # crea la fila y a continuación mete los datos
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())


    def cargarCliente(self):
        """

        Carga los datos de un cliente cuando se clicka en la tabla

        :return: None
        :rtype: None

        """
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni;')
        query.bindValue(':dni', dni)
        var.ui.editCodigoCliente.setText(str(dni))
        if query.exec_():
            while query.next():
                var.ui.editApellidosVentas.setText(str(query.value(2)))
                var.ui.lblCodigoCli.setText(str(query.value(0)))
                var.ui.editCliAlta.setText(query.value(4))
                var.ui.editDireccion.setText(query.value(5))
                var.ui.cmbProvincia.setCurrentText(str(query.value(6)))
                var.ui.spinEdad.setValue(query.value(9))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbFemenino.setChecked(True)
                    var.ui.rbMasculino.setChecked(False)
                else:
                    var.ui.rbMasculino.setChecked(True)
                    var.ui.rbFemenino.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

    def bajaCli(dni):
        """

        Módulo que da de baja a un cliente.

        :param dni: dni del cliente
        :type dni: string
        :return: None
        :rtype: None

        Da de baja a un cliente con el dni pasado. Muestra los datos pasados. Muestra un mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni=:dni')  # Coge el texto del DNI y elimina al cliente con ese DNI
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente eliminado')
        else:
            print('Error eliminar clientes', query.lastError().text())

    def modifCli(codigo, newdata):
        """

        Modulo que modifica los datos del cliente

        :param codigo: codigo del cliente
        :type codigo: string
        :param newdata: datos actualizados
        :type newdata: lista
        :return: None
        :rtype: None

        Se actualizan los datos pasados en la lista del cliente con el codigo dado. En realidad coge todos los datos que
        hay en los widgets. Muestra mensaje en la barra de estado.

        """

        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago, edad=:edad where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', str(newdata[8]))
        if query.exec_():
            print('Cliente modificado')
            var.ui.lblstatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())

    def buscaCli(dni):
        """

        Módulo que busca cliente y carga sus datos en la pantalla cliente.

        :param dni: dni del cliente a buscar
        :type dni: string
        :return: None
        :rtype: None

        Busca en la base de datos el cliente con ese dni y carga los datos en los widgets, si existe.

        """
        try:
            op = True
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select * from clientes where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    var.ui.editApelidos.setText(str(query.value(2)))
                    var.ui.editNome.setText(str(query.value(3)))
            Conexion.mostrarClientes(op)

        except Exception as error:
            print('Error BuscaCli: %s' % str(error))

    def altaPro(newpro):
        """

        Módulo que da de alta un producto.

        :param producto: datos del producto
        :type producto: lista
        :return: None
        :rtype: None

        Muestra mensaje de resultado en la statusbar.
        Rescarga la tablaPro

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into articulos (nombre, precio_unidad,stock)'
            'VALUES (:nombre, :precio,:stock)')
        query.bindValue(':nombre', str(newpro[0]))
        query.bindValue(':precio', str(newpro[1]))
        query.bindValue(':stock', str(newpro[2]))

        if query.exec_():
            print("Inserción Correcta")
            Conexion.mostrarProductos()
            var.ui.lblstatus.setText('Inserción correcta')
        else:
            print("Error Alta Producto: ", query.lastError().text())

    def mostrarProductos(self):
        """

        Módulo que carga los productos en la tablaPro

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()

        query.prepare('select codigo, nombre, precio_unidad from articulos;')

        if query.exec_():
            while query.next():
                codigo = (query.value(0))
                nombre = query.value(1)
                precio = query.value(2)

                var.ui.tablaPro.setRowCount(index + 1)  # crea la fila y a continuación mete los datos
                var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tablaPro.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                index += 1
        else:
            print("Error mostrar Productos: ", query.lastError().text())

    def cargarProducto(self):
        """

        Modulo que carga los valores de los productos desde la bd a los edit de la ventana de productos

        :return: None

        """
        codigo = var.ui.lblCodigoPro.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from articulos where codigo = :codigo;')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            while query.next():
                var.ui.editNombrePro.setText(str(query.value(1)))
                var.ui.editPrecioPro.setText(str(query.value(2)))
                var.ui.editStock.setText(str(query.value(3)))

    def bajaPro(codigoPro):
        """

        Modulo que elemina un producto de la base de datos recibiendo el código del producto

        :param a: Codigo del producto a eliminar
        :type a: Integer
        :return:

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'delete from articulos where codigo=:codigoPro')  # Coge el texto del DNI y elimina al cliente con ese DNI
        query.bindValue(':codigoPro', codigoPro)
        if query.exec_():
            var.ui.lblstatus.setText('Producto eliminado')
            Conexion.mostrarProductos()
        else:
            print('Error eliminar producto', query.lastError().text())

    def modifProducto(codigo, newdata):
        """

        Modulo que recibe el codigo de un producto y valores nuevos del mismo para realizar la actualizacion de esos valores en la base de datos

        :param a: Codigo del producto a modificar
        :type a: Integer
        :param newdata: Valores nuevos a actualizar en el producto
        :type newdata: Coleccion de Strings
        :return: None

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update articulos set nombre=:nombre, precio_unidad=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', str(newdata[0]))
        query.bindValue(':precio', str(newdata[1]))
        query.bindValue(':stock', str(newdata[2]))
        if query.exec_():
            print('Producto modificado')
            var.ui.lblstatus.setText('Producto con codigo ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar Producto: ", query.lastError().text())

    def obtenCodPrec(articulo):
        """

        Modulo que a partir del nombre de un articulo, busca en la base de datos su codigo y precio por unidad

        :param a: String nombre del articulo
        :type a: String
        :return: Codigo y precio unidad del producto
        :rtype: Listra

        """
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio_unidad from articulos where nombre = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                dato = [str(query.value(0)), str(query.value(1))]
        return dato

    def altaVenta(self):
        """

        Modulo que inserta una venta en la base de datos y carga los datos de la venta en la tablaFacturar

        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into ventas (codfactventa, codarticventa, cantidad, precio) VALUES (:codfactventa, :codarticventa,'
            ' :cantidad, :precio )')
        query.bindValue(':codfactventa', int(var.venta[0]))
        query.bindValue(':codarticventa', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))
        row = var.ui.tablaFacturar.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tablaFacturar.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tablaFacturar.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tablaFacturar.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tablaFacturar.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row = row + 1
            var.ui.tablaFacturar.insertRow(row)
            var.ui.tablaFacturar.setCellWidget(row, 1, var.cmbfacturar)
            var.ui.tablaFacturar.scrollToBottom()
            Conexion.cargarCmbventa(var.cmbfacturar)
        else:
            print("Error alta venta: ", query.lastError().text())

    def cargarCmbventa(cmbfacturar):
        """

        Modulo que carga los nombres de los productos en el comboBox de la tabla Facturar que recibe

        :param a: ComboBox de los nombres de los productos
        :type a: ComboBox
        :return: None

        """
        var.cmbfacturar.clear()
        query = QtSql.QSqlQuery()
        var.cmbfacturar.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                var.cmbfacturar.addItem(str(query.value(1)))

    def listadoVentasfac(codfac):
        """

        Modulo que recibe el codigo de la factura y carga los datos de esa factura en la tablaFacturar

        :param a: Codigo de la factura
        :type a: Integer
        :return: None

        """

        try:
            var.ui.tablaFacturar.clearContents()
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfactventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tablaFacturar.setRowCount(index + 1)
                    var.ui.tablaFacturar.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select nombre, precio_unidad from articulos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            precio = query1.value(1)
                            var.ui.tablaFacturar.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tablaFacturar.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tablaFacturar.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio) + '€'))
                            var.ui.tablaFacturar.setItem(index, 4, QtWidgets.QTableWidgetItem(str(subtotal) + '€'))
                            var.ui.tablaFacturar.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
                # ventas.Ven tas.prepararTablaventas(index)
            if int(index) > 0:
                ventas.ventas.prepararventas(index)
            else:

                var.ui.tablaFacturar.setRowCount(0)
                ventas.ventas.prepararventas(0)
            var.ui.lblSubtotal.setText(str(var.subfac))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblIVA.setText(str(var.iva))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblTotal.setText(str(var.fac))
        except Exception as error:
            print('Error listadoVentasfac: %s ' % str(error))

    def anulaVenta(codVenta):
        """

        Modulo que recibe el codigo de una venta y la elimina de la base de datos

        :param a: Codigo de la venta a eliminar
        :type a: Integer
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codVenta')
        query.bindValue(':codVenta', codVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
            ventas.ventas.mostrarVentasfac()
        else:
            print("Error baja venta: ", query.lastError().text())
