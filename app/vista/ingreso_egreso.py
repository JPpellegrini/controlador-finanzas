from dataclasses import dataclass
from datetime import datetime

from PyQt5 import QtCore, QtWidgets, QtGui

from app.ui.ingreso_egreso import Ui_VentanaIngresoEgreso


@dataclass
class TransaccionDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: datetime


@dataclass
class TipoCategoriaDTO:
    nombre: str
    id: int


class ModeloComboBox(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.__data = []

    def update_data(self, data):
        self.modelReset.emit()
        self.__data = data

    def setPlaceholderText(self, nombre):
        self.__place_holder_text = nombre

    def data(self, index: QtCore.QModelIndex, role):
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            return self.__data[row].nombre

        if role == QtCore.Qt.UserRole:
            return self.__data[row].id

    def rowCount(self, index):
        return len(self.__data)

    def columnCount(self, parent):
        return 1


class VentanaIngresoEgreso(QtWidgets.QDialog):
    registrar = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_VentanaIngresoEgreso()
        self.__setupUi()

    def __setupUi(self):
        self.__ui.setupUi(self)

        self.__modelo_combobox_tipo = ModeloComboBox()
        self.__modelo_combobox_categoria = ModeloComboBox()

        self.__ui.combobox_tipo_transaccion.setModel(self.__modelo_combobox_tipo)
        self.__ui.combobox_categorias.setModel(self.__modelo_combobox_categoria)

    def on_button_aceptar(self):
        self.registrar.emit()

    def __set_label_error(self, color, mensaje):
        self.__ui.label_error.setStyleSheet(f"color: {color}")
        self.__ui.label_error.setText(mensaje)

    def __limpiar(self):
        self.__ui.line_monto.clear()
        self.__modelo_combobox_tipo.update_data([])
        self.__modelo_combobox_categoria.update_data([])
        self.__ui.text_descripcion.clear()
        self.__ui.calendar_fecha.setSelectedDate(QtCore.QDate.currentDate())
        self.__ui.label_error.setText("")

    def closeEvent(self, evnt):
        self.__limpiar()

    def mostrar_error(self, error):
        self.__set_label_error("red", str(error))

    def actualizar_tipos_transaccion(self, tipos):
        self.__modelo_combobox_tipo.update_data(tipos)

    def actualizar_categorias(self, categorias):
        self.__modelo_combobox_categoria.update_data(categorias)

    def obtener_transaccion(self):
        monto = self.__ui.line_monto.text()
        id_tipo = self.__ui.combobox_tipo_transaccion.currentData(QtCore.Qt.UserRole)
        id_categoria = self.__ui.combobox_categorias.currentData(QtCore.Qt.UserRole)
        descripcion = self.__ui.text_descripcion.toPlainText()
        selected_date = self.__ui.calendar_fecha.selectedDate().toPyDate()
        current_datetime = datetime.now()
        fecha = current_datetime.replace(
            year=selected_date.year, month=selected_date.month, day=selected_date.day
        )
        return TransaccionDTO(monto, id_tipo, id_categoria, descripcion, fecha)


class VentanaIngreso(VentanaIngresoEgreso):
    def __init__(self, parent=None):
        VentanaIngresoEgreso.__init__(self, parent)
        self.setWindowTitle("Ingreso")


class VentanaEgreso(VentanaIngresoEgreso):
    def __init__(self, parent=None):
        VentanaIngresoEgreso.__init__(self, parent)
        self.setWindowTitle("Egreso")


if __name__ == "__main__":
    import sys

    tipos = (TipoCategoriaDTO("efectivo", 1), TipoCategoriaDTO("tarjeta", 2))
    categorias = (TipoCategoriaDTO("comida", 1), TipoCategoriaDTO("combustible", 2))

    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaIngresoEgreso()
    ventana.registrar.connect(lambda: print(ventana.obtener_transaccion()))
    ventana.actualizar_tipos_transaccion(tipos)
    ventana.actualizar_categorias(categorias)
    ventana.show()

    app.exec()