from PyQt5.QtGui import QFont

import var, conexion
from PyQt5 import QtWidgets, QtSql


class ventas():
    def prepararventas(index):
        """

        Modulo que prepara la tablaFacturar y le agrega el comboBox

        :param index: Posicion inicial
        :type index: Integer
        :return: None

        """
        try:
            var.cmbfacturar = QtWidgets.QComboBox()
            var.cmbfacturar.setFont(QFont('Arial', 8))
            var.ui.tablaFacturar.setRowCount(index + 1)
            var.ui.tablaFacturar.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tablaFacturar.setCellWidget(index, 1, var.cmbfacturar)
            var.ui.tablaFacturar.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tablaFacturar.setItem(index, 3, QtWidgets.QTableWidgetItem())
            query = QtSql.QSqlQuery()
            var.cmbfacturar.addItem('')
            query.prepare('select nombre,precio_unidad from articulos order by nombre')
            if query.exec_():
                while query.next():
                    var.cmbfacturar.addItem(str(query.value(0)))
        except Exception as error:
            print('Error prepararventas: %s ' % str(error))

    def abrirCalendarVentas(self):
        """

        Modulo que abre la ventana del calendario

        :return: None

        """
        try:
            var.dlgcalendar.show()
            var.fecha = 1
        except Exception as error:
            print('Error: %s ' % str(error))

    def crearFactura(self):
        """

        Modulo que recoge los datos de una factura de los edit y crea la factura en la BD

        :return: None

        """
        if var.ui.editFechaFactura.text() != '' and var.ui.editCodigoCliente.text() != '' and var.ui.editApellidosVentas.text() != '' and var.ui.editFechaFactura.text() != '':
            factura = []
            datos = [var.ui.editFechaFactura, var.ui.editCodigoCliente, var.ui.editApellidosVentas]
            for i in datos:
                factura.append(i.text())
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (fecha,dni,apellidos) VALUES (:fecha,:dni,:apellidos)')
            query.bindValue(':fecha', str(factura[0]))
            query.bindValue(':dni', str(factura[1]))
            query.bindValue(':apellidos', str(factura[2]))
            if query.exec_():
                ventas.mostrarFactura(self)
            ventas.prepararventas(0)

    def mostrarFactura(self):
        """

        Modulo que muestra las facturas guardadas en la BD en la tablaFacturas

        :return: None

        """
        try:
            index = 0
            cliente = var.ui.editCodigoCliente.text()
            query = QtSql.QSqlQuery()
            if cliente != '':
                var.ui.tablaFacturas.clearContents()
                query.prepare('select codfact,fecha from facturas where dni=:dni')
                query.bindValue(':dni', cliente)
            else:
                query.prepare('select codfact,fecha from facturas')
            var.ui.tablaFacturas.setRowCount(index)
            var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(""))
            var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(""))
            if query.exec_():

                while query.next():
                    cod = query.value(0)
                    fecha = query.value(1)
                    var.ui.tablaFacturas.setRowCount(index + 1)
                    var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(cod)))
                    var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fecha))
                    index += 1
        except Exception as error:
            print('Error mostrarFactura: %s ' % str(error))

    def limpiarFacturas(self):
        """

        Modulo que limpia los edit de la ventana Facturacion

        :return: None

        """
        try:
            var.ui.editFechaFactura.setText('')
            var.ui.editCodigoCliente.setText('')
            var.ui.editApellidosVentas.setText('')
            var.ui.lblCodigoFactura.setText('')
            ventas.mostrarFactura(self)
        except Exception as error:
            print('Error limpiarFactura: %s ' % str(error))

    def cargarFactura(self):
        """

        Modulo que carga los datos de una factura seleccionada de la tablaFacturas en los edit de la ventana de Facturacion

        :return: None

        """
        try:
            fila = var.ui.tablaFacturas.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            cod = fila[0]
            var.ui.lblCodigoFactura.setText(str(cod))
            fecha = fila[1]
            query = QtSql.QSqlQuery()
            query.prepare('select dni,apellidos from facturas where codfact=:codfact')
            query.bindValue(':codfact', cod)
            if query.exec_():
                while query.next():
                    dni = query.value(0)
                    apellidos = query.value(1)
                    var.ui.editFechaFactura.setText(fecha)
                    var.ui.editCodigoCliente.setText(dni)
                    var.ui.editApellidosVentas.setText(apellidos)
        except Exception as error:
            print('Error cargarFactura: %s ' % str(error))

    def borrarFactura(self):
        """

        Modulo que borra una factura de la BD

        :return: None

        """
        try:
            if var.ui.lblCodigoFactura.text() != '':
                cod = var.ui.lblCodigoFactura.text()
                query = QtSql.QSqlQuery()
                query.prepare('delete from facturas where codfact=:codigo')
                query.bindValue(':codigo', cod)
                if query.exec_():
                    var.ui.lblstatus.setText('Factura borrada')
                    ventas.mostrarFactura(self)
                    ventas.limpiarFacturas(self)

        except Exception as error:
            print('Error borrarFactura: %s ' % str(error))

    def altasFacturacion(self):
        """

        Modulo que da de alta una venta asociada a una factura en la tablaFacturar y llama al metodo altaVenta de la clase Conexion para darla de alta en la BD

        :return: None

        """
        try:
            var.subfac = 0.00
            var.venta = []
            codfac = var.ui.lblCodigoFactura.text()
            var.venta.append(int(codfac))
            articulo = var.cmbfacturar.currentText()
            dato = conexion.Conexion.obtenCodPrec(articulo)
            var.venta.append(int(dato[0]))
            var.venta.append(articulo)
            row = var.ui.tablaFacturar.currentRow()
            cantidad = var.ui.tablaFacturar.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            var.venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            var.venta.append(round(float(precio), 2))
            subtotal = round(float(cantidad) * float(dato[1]), 2)
            var.venta.append(subtotal)
            var.venta.append(row)
            if codfac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta(self)
                var.subfac = round(float(subtotal) + float(var.subfac), 2)
                var.ui.lblSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIVA.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
                ventas.mostrarVentasfac(self)
            else:
                var.ui.lblstatus.setText('Faltan Datos de la Factura')
        except Exception as error:
            print('Error altasFacturacion: %s ' % str(error))

    def mostrarVentasfac(self):
        """

        Modulo que llama a listadoVentasfac para cargar las ventas y a cargarCmbventa para cargar el comboBox de la tabla Facturar

        :return: None

        """
        try:
            var.cmbfacturar = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa(var.cmbfacturar)
            codfac = var.ui.lblCodigoFactura.text()
            conexion.Conexion.listadoVentasfac(codfac)

        except Exception as error:
            print('Error mostrarVentasfac: %s' % str(error))



    def mostrarFacturacion(self):
        """

        Modulo que muestra

        :return: None

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codventa,codarticventa, cantidad, precio from ventas')
            query2 = QtSql.QSqlQuery()
            query2.prepare('select nombre from articulos where codigo=:codigo')

            index = 0
            if query.exec_():
                while query.next():
                    query2.bindValue(':codigo', query.value(1))
                    if query2.exec_():
                        while query2.next():
                            codArtc = query.value(0)
                            var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(codve))
                    codve = query.value(0)
                    cantidad = query.value(2)
                    precio = query.value(3)
                    var.ui.tablaCli.setRowCount(index + 1)  # crea la fila y a continuación mete los datos
                    var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(codve))
                    var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(cantidad))
                    var.ui.tablaCli.setItem(index, 3, QtWidgets.QTableWidgetItem(precio))
                    index += 1
        except Exception as error:
            print('Error mostrarFacturacion: %s ' % str(error))

    def anularVenta(self):
        """

        Modulo que recoge los datos de la venta de los elementos seleccionados de la tablaFacturar y los pasa a anulaVenta de la clase Conexión, para eliminar la venta

        :return: None
        :rtype: None

        """
        try:
            fila = var.ui.tablaFacturar.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            conexion.Conexion.anulaVenta(codventa)
            ventas.mostrarVentasfac(self)

        except Exception as error:
            print('Error anularVenta: %s' % str(error))

    def buscarFact(self):
        """

        Modulo que busca las facturas asociadas a un cliente y las visualiza en la tablaFacturas, visualizando solo las facturas vinculadas al cliente

        :return: None
        :rtype: None

        """
        try:
            index = 0
            cliente = var.ui.editCodigoCliente.text()
            var.ui.tablaFacturas.clearContents()
            if cliente != "":
                query = QtSql.QSqlQuery()
                query.prepare('select codfact, fecha from facturas where dni=:dni')
                query.bindValue(':dni', cliente)
                if query.exec_():
                    while query.next():
                        var.ui.tablaFacturas.setRowCount(index + 1)
                        var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                        var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                        index += 1


        except Exception as error:
            print('Error buscarFact: %s' % str(error))

        except Exception as error:
            print('Error anularVenta: %s' % str(error))
