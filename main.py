from PyQt5 import QtPrintSupport,QtSql

from ventana import *
from vensalir import *
from vencalendar import *
from datetime import datetime
from venaviso import *
from ventanaAbout import *
import sys
import var, events,clients,conexion,productos,printer,ventas

class main(QtWidgets.QMainWindow):

    def __init__(self):
        super(main,self).__init__()
        var.ui=Ui_VenPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir=DialogSalir()
        var.dlgcalendar=DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()
        var.filedlimprimir=PrintDialogAbrir()
        var.dlgaviso=DialogAviso()
        op=False
        """BOTONES"""
        QtWidgets.QAction(self).triggered.connect(self.close)
        """var.ui.butAceptar.clicked.connect(events.Eventos.Saludo)"""
        """---------------PRODUCTOS--------------"""
        var.ui.btnSalirPro.clicked.connect(events.Eventos.Salir)
        var.ui.btnAltaPro.clicked.connect(productos.Productos.AltaProductos)
        var.ui.btnBajaPro.clicked.connect(productos.Productos.bajaProducto)
        var.ui.btnModifPro.clicked.connect(productos.Productos.modifProducto)
        var.ui.btnLimpiarPro.clicked.connect(productos.Productos.limpiarPro)
        var.ui.tablaPro.clicked.connect(productos.Productos.cargarPro)
        var.ui.tablaPro.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        #var.ui.actionAbout.triggered.connect(events.Eventos.AvisoAbout)




        """--------------------------------------"""
        var.ui.btnFechaFactura.clicked.connect(ventas.ventas.abrirCalendarVentas)
        var.ui.btnReloadFact.clicked.connect(ventas.ventas.limpiarFacturas)
        var.ui.btnReloadFact.clicked.connect(ventas.ventas.prepararventas)
        var.ui.btnBuscarFac.clicked.connect(ventas.ventas.buscarFact)

        """--------------------------------------"""
        var.ui.actionInforme_Clientes.triggered.connect(printer.Printer.reportCli)
        var.ui.actionInforme_Productos.triggered.connect(printer.Printer.reportProductos)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.actionInforme_Facturas_Cliente.triggered.connect(printer.Printer.reportFactCli)
        var.ui.actionrestarurarBD.triggered.connect(events.Eventos.restaurarBD)
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)

        var.ui.editDni.editingFinished.connect(events.Eventos.validoDNI)
        var.ui.toolbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.toolbarArchivo.triggered.connect(events.Eventos.AbrirDir)
        var.ui.ToolbarImprimir.triggered.connect(events.Eventos.AbrirImprimir)
        var.ui.toolbarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.actionImprimir.triggered.connect(events.Eventos.AbrirImprimir)
        var.ui.cmbProvincia.activated[str].connect(clients.Clients.selProv)
        var.ui.btnCalendar.clicked.connect(clients.Clients.abrirCalendar)

        var.ui.tablaCli.clicked.connect(clients.Clients.cargarCli)
        var.ui.tablaCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) #coge toda la fila de tablaCli
        var.ui.btnAltaCli.clicked.connect(clients.Clients.AltaClientes)

        var.ui.btnLimpiarCli.clicked.connect(clients.Clients.limpiarCli)
        var.rbtsex=(var.ui.rbFemenino, var.ui.rbMasculino)

        var.ui.btnBajaCli.clicked.connect(clients.Clients.bajaCliente)
        var.ui.btnModifCli.clicked.connect(clients.Clients.modifCliente)
        var.ui.btnReloadCli.clicked.connect(clients.Clients.reloadCli)
        var.ui.btnBuscarCli.clicked.connect(clients.Clients.buscarCli)

        var.ui.lblFecha.setText(datetime.strftime(datetime.now(), "%d/%m/%Y"))
        var.ui.statusBar.addPermanentWidget(var.ui.lblstatus,1) #Agrega al status bar el lblstatus.
        var.ui.statusBar.addPermanentWidget(var.ui.lblFecha, 0) #Agrega al status bar la fecha.


        var.ui.lblstatus.setText("Bienvenido a 2º DAM")


        for i in var.rbtsex:
            i.toggled.connect(clients.Clients.selSexo)
        var.chkpago=(var.ui.chkEfectivo,var.ui.chkTarjeta,var.ui.chkTransferencia)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clients.selPago)


        var.ui.tablaCli.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        var.ui.tablaPro.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        var.ui.tablaFacturas.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        var.ui.tablaFacturar.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        events.Eventos.cargarProv(self)

        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(op)
        conexion.Conexion.mostrarProductos()
        ventas.ventas.prepararventas(0)
        var.ui.btnFacturar.clicked.connect(ventas.ventas.crearFactura)
        var.ui.btnAnular.clicked.connect(ventas.ventas.borrarFactura)
        ventas.ventas.mostrarFactura(self)
        var.ui.tablaFacturas.clicked.connect(ventas.ventas.cargarFactura)
        var.ui.tablaFacturas.clicked.connect(ventas.ventas.mostrarVentasfac)
        var.ui.btnEliminarPro.clicked.connect(ventas.ventas.anularVenta)
        var.ui.tablaFacturas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tablaFacturar.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.btnAdPro.clicked.connect(ventas.ventas.altasFacturacion)
        var.ui.btnBuscarFac.clicked.connect(ventas.ventas.mostrarFactura)
        var.ui.actionInforme_Facturas.triggered.connect(printer.Printer.reportFac)
    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir=Ui_venSalir()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).setText('SI')
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.closeSalir)

class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgaviso=Ui_venAviso()
        var.dlgaviso.setupUi(self)
        var.dlgaviso.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText('NO')
        var.dlgaviso.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).setText('SI')
        var.dlgaviso.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(events.Eventos.closeAviso)
        var.dlgaviso.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.validarAviso)
        var.lblAvisoSalir=var.dlgaviso.lblAvisoSalir

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar,self).__init__()
        var.dlgcalendar=Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual=datetime.now().day
        mesactual=datetime.now().month
        anoactual=datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual,mesactual,diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clients.CargarFecha)
        var.dlgcalendar.Calendar.clicked.connect(ventas.ventas)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class PrintDialogAbrir(QtPrintSupport.QPrintDialog):
    def __init__(self):
        super(PrintDialogAbrir, self).__init__()
class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        var.dlgabout = Ui_venAbout()
        var.dlgabout.setupUi(self)
        var.dlgabout.btnBoxCerrar.button(QtWidgets.QDialogButtonBox.Cancel).setText('Cerrar')
        var.dlgabout.btnBoxCerrar.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(events.Eventos.cerrarAvisoAbout)

if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    window = main()
    window.showMaximized()
    sys.exit(app.exec())
