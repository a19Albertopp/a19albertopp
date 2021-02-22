import unittest
import conexion, clients, var
from PyQt5 import QtSql


class MyTestCase(unittest.TestCase):

    def test_conexion(self):
        value = conexion.Conexion.db_connect(var.filebd)
        msg = 'Conexión no realizada'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni = '00000000T'
        value = clients.Clients.validarDni(dni)
        msg = 'Error validar DNI'
        self.assertTrue(value, msg)

    def test_fact(self):

