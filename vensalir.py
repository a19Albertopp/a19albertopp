# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vensalir.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import var

class Ui_venSalir(object):
    def setupUi(self, venSalir):
        venSalir.setObjectName("venSalir")
        venSalir.resize(330, 164)
        venSalir.setModal(True)
        self.btnBoxSalir = QtWidgets.QDialogButtonBox(venSalir)
        self.btnBoxSalir.setGeometry(QtCore.QRect(90, 110, 156, 23))
        self.btnBoxSalir.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.btnBoxSalir.setObjectName("btnBoxSalir")
        var.lblMenSalir = QtWidgets.QLabel(venSalir)
        var.lblMenSalir.setGeometry(QtCore.QRect(80, 20, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        var.lblMenSalir.setFont(font)
        var.lblMenSalir.setObjectName("lblMenSalir")
        self.label = QtWidgets.QLabel(venSalir)
        self.label.setGeometry(QtCore.QRect(10, 30, 51, 41))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/icono_aviso.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(venSalir)
        QtCore.QMetaObject.connectSlotsByName(venSalir)

    def retranslateUi(self, venSalir):
        _translate = QtCore.QCoreApplication.translate
        venSalir.setWindowTitle(_translate("venSalir", "Desea salir"))
        var.lblMenSalir.setText(_translate("venSalir", "¿Esta seguro que desea salir?"))
import aviso_salir_rc
