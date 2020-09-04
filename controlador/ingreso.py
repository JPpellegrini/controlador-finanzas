import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaIngreso, TipoCategoriaDTO
from modelo.modelo import ServiceIngreso, TransaccionDTO, MontoError


class ControladorIngreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.__modelo = ServiceIngreso()
        self.__vista = VentanaIngreso(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        ingreso = self.__vista.obtener_transaccion()
        try:
            self.__modelo.registrar_ingreso(TransaccionDTO(ingreso.monto, ingreso.id_tipo_transaccion, ingreso.id_categoria,
                                                            ingreso.descripcion, ingreso.fecha))
            self.__vista.verificar_error()
            self.actualizar_balance.emit()
        except MontoError as error:
            self.__vista.verificar_error(error)
    
    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        tipos = [TipoCategoriaDTO(tipo.nombre, tipo.id) for tipo in tipos_categorias["tipos"]]
        categorias = [TipoCategoriaDTO(categoria.nombre, categoria.id) for categoria in tipos_categorias["categorias"]]
        self.__vista.actualizar_tipos_transaccion(tipos)
        self.__vista.actualizar_categorias(categorias)
        self.__vista.show()


if __name__ == "__main__":
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorIngreso()
    controlador.show_vista()
    app.exec()