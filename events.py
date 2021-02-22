import os
import shutil
import zipfile

import var, conexion, ventas
import sys
import clients
from PyQt5 import QtWidgets
from datetime import datetime


class Eventos():
    """EVENTOS GENERALES"""

    def Salir(event):
        """
        Método que cierra el programa

        :param event: evento salir
        :type event: event
        :return: None
        :rtype: None

        Abre la ventana salir y cierra el programa si se clicka el botón aceptar

        """

        try:
            var.lblMenSalir.setText("Salir de Xestion")
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                sys.exit()
            else:
                var.dlgsalir.hide()
                event.ignore()


        except Exception as error:
            print('Error salir: %s' % str(error))

            """
            EVENTOS CLIENTES
            """

    def closeSalir(event):
        """

        Módulo que cierra la ventana salir

        :return: None
        :rtype: None

        """
        try:
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                var.dlgsalir.hide()

        except Exception as error:
            print('Error closesalir: %s' % str(error))


    def validoDNI(self):
        """

        Módulo que según sea correcto el dni, muestra una imagen distinta

        :return: None

        Si es falso escribe en el label una X roja, y si es verdadero escribe una V verde
        """
        try:
            dni = var.ui.editDni.text()
            if clients.Clients.validarDni(dni):
                var.ui.lblValido.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValido.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:
                var.ui.lblValido.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValido.setText('X')
                var.ui.editDni.setText(dni.upper())
                # clients.Clients.limpiarCli()

        except:
            print('Error módulo escribir valido DNI')
            return None

    def cargarProv(self):
        """
        CARGA LAS PROVIENCIAS AL INICIAR EL PROGRAMA

        """

        try:
            prov = ['', 'A Coruña', 'Ourense', 'Pontevedra', 'Lugo']
            for i in prov:
                var.ui.cmbProvincia.addItem(i)

        except Exception as error:
            print('Error: %s ' % str(error))

    def Backup(self):
        """

                Módulo que realiza una copia de seguridad de la base de datos

                :return: None
                :rtype: None

                Abre una ventana para elegir el directorio donde guardar la copia. Comprime el archivo de la base de datos
                en un archivo zip. Muestra un mensaje en la barra de estado.

                """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.filedlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                    options=option)
            if var.filedlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                var.ui.lblstatus.setText('COPIA DE SEGURIDAD DE BASE DE DATOS CREADA')
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error: %s' % str(error))

    def AbrirDir(self):
        """

        Módulo que abre una ventana para elegir directorio

        :return: None
        :rtype: None

        """
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def AbrirAviso(mensaje):
        """

        Módulo que abre una ventana de aviso

        :param mensaje: mensaje que muestra la ventana
        :type mensaje: string
        :return: bool
        :rtype: True/False

        Abre una ventada de aviso con el mensaje pasado por parámetro. Devuelve un booleano dependiendo de si se ejecuta
        o no.

        """
        try:
            var.lblAvisoSalir.setText(mensaje)
            var.dlgaviso.show()
            var.salir = False
            if var.dlgaviso.exec_():
                var.dlgaviso.hide()
            else:
                var.dlgaviso.hide()
            return var.salir
        except Exception as error:
            print('Error Abrir Aviso: %s ' % str(error))

    def AbrirImprimir(self):
        """

        Módulo que abre la ventana de impresión

        :return: None
        :rtype: None

        """
        try:
            var.filedlimprimir.show()
        except Exception as error:
            print('Error Abrir Imprimir: %s ' % str(error))

    def closeAviso(event):
        """

        Modulo que cierra la ventana de aviso

        :param a: Evento de ventana
        :return: None
        :rtype: None

        """
        try:
            var.validar = False
            var.dlgaviso.show()
            if var.dlgaviso.exec_():
                var.dlgaviso.hide()

        except Exception as error:
            print('Error closeaviso: %s' % str(error))

    def validarAviso(self):
        """

        Modulo que valida la ventana de aviso

        :return: None
        :rtype: None

        """
        var.validar = True
        if var.dlgaviso.exec_():
            var.dlgaviso.hide()

    def restaurarBD(self):
        """

        Modulo que restaura la base de datos

        :return: None

        """
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridade', '', '*.zip',
                                                        options=option)
            if var.filedlgabrir.Accepted and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r')as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            clients.Clients.limpiarCli(self)
            conexion.Conexion.mostrarProductos()
            conexion.Conexion.mostrarClientes(False)
            ventas.ventas.mostrarVentasfac(self)
            ventas.ventas.mostrarFacturacion(self)
            ventas.ventas.limpiarFacturas(self)
            ventas.ventas.prepararventas(self)

        except Exception as error:
            print('Error restaurarBD: %s' % str(error))
