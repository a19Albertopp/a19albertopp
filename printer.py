from reportlab.pdfgen import canvas
from PyQt5 import QtSql
import os, var
from datetime import datetime
from reportlab.lib.pagesizes import A4
import conexion


class Printer():

    def Cabecera(self):

        logo = conexion.Conexion.resource_path('img\logo.png')
        var.rep.drawImage(logo, 450, 752)
        var.rep.setTitle('INFORMES')
        var.rep.setAuthor('a19Albertopp')
        var.rep.setFont('Helvetica', size=10)
        var.rep.line(45, 820, 525, 820)
        var.rep.line(45, 745, 525, 745)
        textcif = 'CIF: A000000H'
        textnom = 'IMPORTACIONES Y EXPORTACIONES TEIS S.L.'
        textdir = 'Avda. de Galicia, 101 - Vigo C.P.: 36216'
        texttelf = '886 12 04 64'
        var.rep.drawString(50, 805, textcif)
        var.rep.drawString(50, 790, textnom)
        var.rep.drawString(50, 775, textdir)
        var.rep.drawString(50, 760, texttelf)

    def pie(textlistado):
        try:
            var.rep.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=6)
            var.rep.drawString(460, 40, str(fecha))
            var.rep.drawString(270, 40, str('Pagina %s' % var.rep.getPageNumber()))
            var.rep.drawString(50, 40, str(textlistado))
        except Exception as error:
            print('Error pie: %s ' % str(error))

    def cabeceracli(self):

        try:
            var.rep.setFont('Helvetica-Oblique', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(230, 734, textlistado)
            var.rep.line(45, 730, 525, 730)
            itempro = ['COD', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45, 710, itempro[0])
            var.rep.drawString(90, 710, itempro[1])
            var.rep.drawString(180, 710, itempro[2])
            var.rep.drawString(325, 710, itempro[3])
            var.rep.drawString(465, 710, itempro[4])
            var.rep.line(45, 703, 525, 703)

        except Exception as error:
            print('Error cabecerainf: %s ' % str(error))

    def cabeceraFactCli(self):

        try:
            var.rep.setFont('Helvetica-Oblique', size=9)
            textlistado = 'FACTURAS DEL CLIENTE'
            cli = ['NOMBRE', 'DNI']
            var.rep.drawString(45, 730, cli[0])
            var.rep.drawString(60, 715, cli[1])
            var.rep.drawString(230, 700, textlistado)
            var.rep.line(45, 690, 525, 690)
            itempro = ['Nº FACTURA', 'FECHA', 'TOTAL']
            var.rep.drawString(45, 678, itempro[0])
            var.rep.drawString(250, 678, itempro[1])
            var.rep.drawString(400, 678, itempro[2])
            var.rep.line(45, 670, 525, 670)
            codcli = var.ui.editCodigoCliente.text()
            var.rep.drawString(100, 715, codcli)
            query = QtSql.QSqlQuery()
            query.prepare('select nombre from clientes where dni=:dni')
            query.bindValue(':dni', codcli)
            if query.exec_():
                while query.next():
                    nombre = query.value(0)
                    nombre = nombre + " " + var.ui.editApellidosVentas.text()
                    var.rep.drawString(100, 730, nombre)

        except Exception as error:
            print('Error cabeceraPro: %s ' % str(error))

    def cabeceraPro(self):

        try:
            var.rep.setFont('Helvetica-Oblique', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(230, 734, textlistado)
            var.rep.line(45, 730, 525, 730)
            itempro = ['CODIGO', 'NOMBRE', 'PRECIO', 'STOCK']
            var.rep.drawString(45, 710, itempro[0])
            var.rep.drawString(180, 710, itempro[1])
            var.rep.drawString(325, 710, itempro[2])
            var.rep.drawString(480, 710, itempro[3])
            var.rep.line(45, 703, 525, 703)


        except Exception as error:
            print('Error cabeceraFactCli: %s ' % str(error))

    def reportFactCli(self):
        try:
            precio_total = 0
            textlistado = "LISTADO FACTURAS CLIENTES"
            var.rep = canvas.Canvas(conexion.Conexion.resource_path('informes/listadofactcli.pdf'))
            Printer.Cabecera(self)
            Printer.cabeceraFactCli(self)
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codfact, fecha from facturas where dni=:dni')
            query.bindValue(':dni', var.ui.editCodigoCliente.text())
            var.rep.setFont('Helvetica', size=10)
            var.rep.drawString(330, 60, 'TOTAL FACTURACION:')
            if query.exec_():
                i = 50
                j = 650
                while query.next():

                    if j <= 80:
                        var.rep.showPage()
                        Printer.Cabecera()
                        Printer.cabeceracli()
                        Printer.pie()
                        i = 50
                        j = 690
                    precio = 0
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 200, j, str(query.value(1)))
                    query2 = QtSql.QSqlQuery()
                    query2.prepare('select cantidad,precio from ventas where codfactventa=:codfact')
                    query2.bindValue(':codfact', str(query.value(0)))
                    if query2.exec_():
                        while query2.next():
                            cantidad = query2.value(0)
                            valor = query2.value(1)
                            precio = float(valor) * int(cantidad) * 1.21 + precio
                            precio = round(precio, 2)
                    var.rep.drawString(i + 350, j, str(precio) + '€')
                    precio_total = precio_total + precio
                    j -= 25
                var.rep.drawString(450, 60, str(precio_total) + '€')
            var.rep.save()
            rootPath = conexion.Conexion.resource_path(".\\informes")
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadofactcli.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont += 1
        except Exception as error:
            print('Error reportFactCli: %s ' % str(error))

    def reportCli(self):
        try:
            textlistado = 'LISTADO CLIENTES'
            var.rep = canvas.Canvas(conexion.Conexion.resource_path('informes/listadoclientes.pdf'))
            Printer.Cabecera(self)
            Printer.cabeceracli(self)
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo,dni,apellidos,nombre,fechalta from clientes order by apellidos,nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50
                j = 690
                while query.next():
                    if j <= 80:
                        var.rep.showPage()
                        Printer.Cabecera()
                        Printer.cabeceracli()
                        Printer.pie()
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 30, j, str(query.value(1)))
                    var.rep.drawString(i + 130, j, str(query.value(2)))
                    var.rep.drawString(i + 280, j, str(query.value(3)))
                    var.rep.drawRightString(i + 470, j, str(query.value(4)))
                    j -= 25

            var.rep.save()
            rootPath = conexion.Conexion.resource_path(".\\informes")
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont += 1

        except Exception as error:
            print('Error reportCli: %s ' % str(error))

    def reportProductos(self):
        try:
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep = canvas.Canvas(conexion.Conexion.resource_path('informes/listadoproductos.pdf'), pagesize=A4)
            Printer.Cabecera(self)
            Printer.pie(textlistado)
            Printer.cabeceraPro(self)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre,precio_unidad,stock from articulos order by nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50
                j = 690
                while query.next():
                    if j <= 80:
                        var.rep.showPage()
                        Printer.Cabecera(self)
                        Printer.pie(textlistado)
                        Printer.cabeceraPro(self)
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i - 5, j, str(query.value(0)))
                    var.rep.drawString(i + 130, j, str(query.value(1)))
                    var.rep.drawString(i + 275, j, str(query.value(2)))
                    var.rep.drawString(i + 435, j, str(query.value(3)))
                    j -= 25

            var.rep.save()
            rootPath = conexion.Conexion.resource_path(".\\informes")
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoproductos.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont += 1

        except Exception as error:
            print('Error reportPro: %s ' % str(error))

    def cabecerafac(codfact):
        try:
            var.rep.setFont('Helvetica-Bold', size=11)
            var.rep.drawString(55, 725, 'Cliente: ')
            var.rep.setFont('Helvetica', size=10)
            var.rep.drawString(50, 650, 'Factura nº : %s' % str(codfact))
            var.rep.line(45, 667, 525, 667)
            var.rep.line(45, 640, 525, 640)
            var.rep.setFont('Helvetica', size=10)
            query = QtSql.QSqlQuery()
            query.prepare('select  fecha,dni from facturas where codfact = :codfact')
            query.bindValue(':codfact', int(codfact))
            if query.exec_():
                while query.next():
                    dni = str(query.value(1))
                    var.rep.drawString(55, 710, 'DNI: %s' % str(query.value(1)))
                    var.rep.drawString(420, 650, 'Fecha: %s' % str(query.value(0)))
            query1 = QtSql.QSqlQuery()
            query1.prepare('select apellidos, nombre, direccion, provincia, formaspago from clientes where dni = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec_():
                while query1.next():
                    var.rep.drawString(55, 695, str(query1.value(0)) + ', ' + str(query1.value(1)))
                    var.rep.drawString(300, 695, 'Formas de Pago: ')
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(300, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',', ' -')))
            var.rep.line(45, 620, 525, 620)
            var.rep.setFont('Helvetica-Bold', size=10)
            temven = ['CodVenta', 'Artículo', 'Cantidad', 'Precio-Unidad(€)', 'Subtotal(€)']
            var.rep.drawString(50, 626, temven[0])
            var.rep.drawString(140, 626, temven[1])
            var.rep.drawString(275, 626, temven[2])
            var.rep.drawString(360, 626, temven[3])
            var.rep.drawString(470, 626, temven[4])
            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160,
                                    'Subtotal:   ' + "{0:.2f}".format(float(var.ui.lblSubtotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:     ' + "{0:.2f}".format(float(var.ui.lblIVA.text())) + ' €')
            var.rep.drawRightString(500, 120,
                                    'Total Factura: ' + "{0:.2f}".format(float(var.ui.lblTotal.text())) + ' €')
        except Exception as error:
            print('Error cabecfac %s' % str(error))

    def reportFac(self):
        try:
            textlistado = 'FACTURA'
            var.rep = canvas.Canvas(conexion.Conexion.resource_path('informes/factura.pdf'), pagesize=A4)
            Printer.Cabecera(self)
            Printer.pie(textlistado)
            codfac = var.ui.lblCodigoFactura.text()
            Printer.cabecerafac(codfac)
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfactventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                i = 70  # valores del eje X
                j = 600  # valores del eje Y
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.Cabecera(self)
                        Printer.pie(textlistado)
                        Printer.cabecerafac(self)
                        i = 70
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    query2 = QtSql.QSqlQuery()
                    query2.prepare('select nombre from articulos where codigo =:codarticventa')
                    query2.bindValue(':codarticventa', str(query.value(1)))
                    if query2.exec_():
                        while query2.next():
                            var.rep.drawString(i + 85, j, str(query2.value(0)))
                    var.rep.drawRightString(i + 225, j, str(query.value(2)))
                    var.rep.drawRightString(i + 335, j, "{0:.2f}".format(float(query.value(3))))
                    subtotal = round(float(query.value(2)) * float(query.value(3)), 2)
                    var.rep.drawRightString(i + 430, j, "{0:.2f}".format(float(subtotal)) + ' €')
                    j = j - 20

            var.rep.save()
            rootPath = conexion.Conexion.resource_path(".\\informes")
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporfac %s' % str(error))
