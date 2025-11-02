"""
Aplicación de Overlay con Guías de Composición Fotográfica
Usando PyQt5 para mayor funcionalidad y control
"""
import sys
from PyQt5.QtWidgets import QApplication
from control_panel import ControlPanel
from overlay_window import OverlayWindow

class CompositionOverlayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Composition Overlay")
        
        # Crear ventana de overlay (siempre al frente)
        self.overlay = OverlayWindow()
        
        # Crear panel de control
        self.control_panel = ControlPanel(self.overlay)
        self.control_panel.show()
        
        # Conectar señal de cierre
        self.control_panel.closed.connect(self.cleanup)
        
    def cleanup(self):
        """Limpieza al cerrar"""
        self.overlay.close()
        
    def run(self):
        """Ejecutar aplicación"""
        return self.app.exec_()


if __name__ == "__main__":
    app = CompositionOverlayApp()
    sys.exit(app.run())
