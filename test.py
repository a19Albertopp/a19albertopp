import unittest
import conexion, clients, var
from PyQt5 import QtSql


class MyTestCase(unittest.TestCase):

    def test_1conexion(self):
        value = conexion.Conexion.db_connect(var.filebd)
        msg = 'Conexión no realizada'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni = '00000000T'
        value = clients.Clients.validarDni(dni)
        msg = 'Error validar DNI'
        self.assertTrue(value, msg)

    def test_fact(self):
        valor = 345.52
        codfac = 23

        try:
            msg = 'Claculos incorrectos'
            var.subfact = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa,codarticventa,cantidad from ventas where codfactventa=:codfact')
            query.bindValue(':codfact', int(codfac))
            if query.exec_():
                while query.next():
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    query1.prepare('select nombre,precio_unidad from articulos where codigo=:codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            precio = query1.value(1)
                            subtotal = round(float(cantidad) * float(precio), 2)
                    var.subfact = round(float(subtotal) + float(var.subfact), 2)
            var.iva = round(float(var.subfact) * 0.21, 2)
            var.fac = round(float(var.iva) + float(var.subfact), 2)
        except Exception as error:
            print('Error lsitado de la tabla de ventas: %s ' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fac), 2), msg)

    def test_codigo_producto(self):
        cod = '588'
        dato = conexion.Conexion.obtenCodPrec('Zapote')
        msg = 'Error Obtener codigo del producto'
        self.assertEqual(dato[0], cod, msg)
