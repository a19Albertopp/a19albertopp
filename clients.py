import var
from PyQt5 import QtWidgets
import conexion, events

class Clients():
    def validarDni(dni):
        """

        Módulo que valida la letra de un dni segñun sea nacional o extranjero

        :param a: dni formato texto
        :return: None
        :rtype: bool

        Pone la letra en mayúsculas, comprueba que son nueve carácteres. Toma los 8 primeros, si es extranjero cambia la letra por un número,
        y aplica el algoritmo de comprobación de la letra basado en la normativa.
        Si es correcto devuelve True, si es falso devuelve False

        """
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control

        except:
            print('Error módulo validar DNI')
            return None

    def selProv(prov):
        """

        Al seleccionar una provincia en el combo de provincias llama al evento activated

        :param a: provincia seleccionada
        :type a: string

        """
        try:
            global vpro
            vpro = prov

        except Exception as error:
            print('Error: %s ' % str(error))

    def CargarFecha(qDate):
        """

        Módulo que carga la fercha marcada en el widgetCalendar

        :param a: Librería Python para formateo de fechas
        :return: None
        :rtype: formato de fechas Python

        A partir de los eventos calendar.clicked.connect al clickear en una fecha, captura y la carga en el widget edit

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.fecha==0:
                var.ui.editCliAlta.setText(str(data))
            elif var.fecha==1:
                var.ui.editFechaFactura.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error: %s ' % str(error))


    def abrirCalendar(self):
        """

        Modulo que abre la ventana del calendario

        """
        try:
            var.dlgcalendar.show()
            var.fecha=0
        except Exception as error:
            print('Error: %s ' % str(error))

    def selSexo(self):
        """

        Módulo que según checkeemos el rbt Fem o Masc, carga el texto correspondiente de Mujer o Hombre
        a la variable var.sex que luego se añade a la lista de los datos del cliente a incluír en la base de datos

        :return: None

        """
        try:
            if var.ui.rbFemenino.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbMasculino.isChecked():
                var.sex = 'Hombre'

        except Exception as error:
            print('Error: %s ' % str(error))

    def selPago(self):
        """

        Checkea que valores de pago selecciona en el checkBox y los añade a una variable lista var.py

        :return:
        :rtype:

        En QtDSesigner se debe agrupar los checkBox en un ButtonGroup

        """
        try:
            var.pay=[]
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                if data.isChecked() and i==0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i==1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i==2:
                    var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error: %s ' % str(error))

    def AltaClientes(self):
        """

        MODULO QUE CARGA LOS DATOS DEL CLIENTE

        :param a: None
        :param b: None
        :return: None

        Se crea una lista que contendra todos los datos del cliente que se introduzcan en los widgets,
        esta lista se pasa como argumento al modulo altaCli del modulo conexion.
        El modulo llama a la funcion mostrarClientes que recarga la tabla con todos los clientes además del nuevo.
        El módulo llama a la funcion limpiarCli que vacía el contenido de los widgets

        """
        try:
            newcli = []
            clitab = []
            client = [var.ui.editDni, var.ui.editApelidos, var.ui.editNome, var.ui.editCliAlta, var.ui.editDireccion]
            k = 0
            for i in client:
                newcli.append(i.text())
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            var.pay2 = Clients.selPago(self)
            newcli.append(var.sex)
            newcli.append(var.pay2)
            newcli.append(var.ui.spinEdad.value())
            if client:

                row = 0
                column = 0
                var.ui.tablaCli.insertRow(row)

                for registro in clitab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tablaCli.setItem(row, column, cell)
                    column += 1


                conexion.Conexion.altaCli(newcli)
            else:
                print('Faltan Datos')

        except Exception as error:
            print('Error alta clientes: %s ' % str(error))

    def limpiarCli(self):
        """

        limpia los datos del formulario cliente

        """

        try:
            client = [var.ui.editDni, var.ui.editApelidos, var.ui.editNome, var.ui.editCliAlta, var.ui.editDireccion] #Son los edit
            for i in range(len(client)):
                client[i].setText('')   #Pone los editText en blanco
            var.ui.grpbtnSex.setExclusive(False) # necesario para los radiobutton
            var.ui.grpbtnPay.setExclusive(False)
            for dato in var.rbtsex:         #para cada radiobutton lo pone en falso
                dato.setChecked(False)
            for data in var.chkpago:        #para cada checkbox lo pone en falso
                data.setChecked(False)
            var.ui.cmbProvincia.setCurrentIndex(0)  #La posicion 0 es vacio
            var.ui.lblValido.setText('')
            var.ui.lblCodigoCli.setText('')
            var.ui.spinEdad.setValue(16)
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def cargarCli(self):
        """

        Módulo que se activa con el evento clicked.connect y setSelectionBehaviour del widget TablaCli

        :return: None
        :rtype: None

        Al generarse el evento se  llama al módulo de Conexión cargarCliente, que devuelve los datos del cliente seleccionado
        haciendo una llamada a la base de datos

        """
        try:
            fila=var.ui.tablaCli.selectedItems()
            client= [var.ui.editDni, var.ui.editApelidos, var.ui.editNome]
            if fila:
                fila=[dato.text() for dato in fila] #coge los datos de una fila de la tablaCli
            for i,dato in enumerate(client):
                dato.setText(fila[i]) #Introduce los datos de fila en los editText de client
            conexion.Conexion.cargarCliente(self)


        except Exception as error:
            print('Error cargar cli: %s ' % str(error))

    def bajaCliente(self):
        """

        Módulo que da de baja un cliente a partir del dni. Además recarga los datos del widget tablaCli con los datos actualizados desde la base de datos

        :return: None
        :rtype: None

        Toma el dni cargado en el widget editDni se lo pasa al módulo bajaCli en la clase conexión y da de baja el cliente.
        Limpia los datos del formulario y recarga la tabla tablaCli

        """
        try:
            var.validar=False
            dni=var.ui.editDni.text()
            mensaje=('Desea eliminar el cliente?')
            if var.ui.editDni.text()!='':
                events.Eventos.AbrirAviso(mensaje)
            if var.validar==True:
                conexion.Conexion.bajaCli(dni)
                conexion.Conexion.mostrarClientes(False)
                Clients.limpiarCli(self)
        except Exception as error:
            print('Error bajar clientes: %s' %str(error))

    def modifCliente(self):
        """

        Modulo para modificar los datos del clietne con un determinado código

        :return: None
        :rtype: None

        A partir del código del cliente, lee los datos de los widgets que se han cargado y modificado,
        llama al módulo modifCli de la clase conexión para actualizar los datos en la BBDD pas,andole una lista con los nuevos datos.
        Vuelve a mostrar la tablaCli actualizada pero no limpia datos de los widget.

        """
        try:
            var.validar=False
            newdata=[]
            client=[var.ui.editDni, var.ui.editApelidos, var.ui.editNome, var.ui.editCliAlta, var.ui.editDireccion]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmbProvincia.currentText()) #Selecciona la provincia
            newdata.append(var.sex)
            var.pay=Clients.selPago(self)
            newdata.append(var.pay)
            newdata.append(var.ui.spinEdad.value())
            cod=var.ui.lblCodigoCli.text()
            mensaje=('Seguro que desea Modificar el Cliente?')
            events.Eventos.AbrirAviso(mensaje)
            if var.validar==True:
                conexion.Conexion.modifCli(cod,newdata)
                conexion.Conexion.mostrarClientes(False)
        except Exception as error:
            print('Error modifClientes: %s' %str(error))


    def reloadCli(self):
        """

        Limpia datos del formulario y recarga la tabla de clientes

        :return: None
        :rtype: None

        """
        try:
            op=False
            Clients.limpiarCli(self)
            conexion.Conexion.mostrarClientes(op)
        except Exception as error:
            print('Error reloadCli: %s' % str(error))

    def buscarCli(self):
        """

        Busca un cliente a partir de un dni que escribe el usuario

        :return: None
        :rtype: None

        Toma el dni del widget editDni y llama a la función buscarCli de la clase Conexión a a que pasa el dni

        """
        try:
            dni=var.ui.editDni.text()
            conexion.Conexion.cargarCliente(self)
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error buscarCli: %s' % str(error))