"""
Ventana de Overlay Transparente con Guías de Composición
"""
from PyQt5.QtWidgets import QWidget, QMenu, QAction
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath
import math


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración de guías
        self.guides = {
            'rule_of_thirds': True,
            'golden_ratio': False,
            'center_lines': False,
            'diagonals': False,
            'golden_spiral': False,
            'grid_4x4': False,
            'grid_5x5': False,
            'safe_areas': False
        }
        
        # Configuración de estilo
        self.guide_color = QColor(255, 255, 255, 180)  # Blanco semi-transparente
        self.line_width = 2
        self.window_opacity = 0.8
        self.fill_opacity = 30  # Para áreas de relleno
        
        # Configuración de la espiral
        self.spiral_offset_x = 0  # Desplazamiento horizontal de la espiral (0-14)
        
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz"""
        # Configurar ventana sin marco y transparente
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Hacer ventana transparente
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        
        # Pantalla completa
        self.showFullScreen()
        
        # Menú contextual
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def paintEvent(self, event):
        """Dibuja las guías de composición"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configurar pen para las líneas
        pen = QPen(self.guide_color, self.line_width)
        painter.setPen(pen)
        
        width = self.width()
        height = self.height()
        
        # Dibujar guías activas
        if self.guides['rule_of_thirds']:
            self.draw_rule_of_thirds(painter, width, height)
            
        if self.guides['golden_ratio']:
            self.draw_golden_ratio(painter, width, height)
            
        if self.guides['center_lines']:
            self.draw_center_lines(painter, width, height)
            
        if self.guides['diagonals']:
            self.draw_diagonals(painter, width, height)
            
        if self.guides['golden_spiral']:
            self.draw_golden_spiral(painter, width, height)
            
        if self.guides['grid_4x4']:
            self.draw_grid(painter, width, height, 4, 4)
            
        if self.guides['grid_5x5']:
            self.draw_grid(painter, width, height, 5, 5)
            
        if self.guides['safe_areas']:
            self.draw_safe_areas(painter, width, height)
    
    def draw_rule_of_thirds(self, painter, width, height):
        """Dibuja la regla de tercios (grid 3x3)"""
        # Líneas verticales
        painter.drawLine(int(width / 3), 0, int(width / 3), height)
        painter.drawLine(int(2 * width / 3), 0, int(2 * width / 3), height)
        
        # Líneas horizontales
        painter.drawLine(0, int(height / 3), width, int(height / 3))
        painter.drawLine(0, int(2 * height / 3), width, int(2 * height / 3))
        
        # Puntos de intersección (puntos fuertes)
        old_pen = painter.pen()
        painter.setPen(QPen(self.guide_color, self.line_width * 3))
        
        points = [
            (width / 3, height / 3),
            (2 * width / 3, height / 3),
            (width / 3, 2 * height / 3),
            (2 * width / 3, 2 * height / 3)
        ]
        
        for x, y in points:
            painter.drawEllipse(QPoint(int(x), int(y)), 5, 5)
        
        painter.setPen(old_pen)
    
    def draw_golden_ratio(self, painter, width, height):
        """Dibuja rectángulos de proporción áurea"""
        phi = 1.618033988749895  # Número áureo
        
        # Líneas verticales
        x1 = width / phi
        x2 = width - x1
        
        painter.drawLine(int(x1), 0, int(x1), height)
        painter.drawLine(int(x2), 0, int(x2), height)
        
        # Líneas horizontales
        y1 = height / phi
        y2 = height - y1
        
        painter.drawLine(0, int(y1), width, int(y1))
        painter.drawLine(0, int(y2), width, int(y2))
        
        # Puntos de intersección
        old_pen = painter.pen()
        painter.setPen(QPen(self.guide_color, self.line_width * 3))
        
        points = [
            (x1, y1), (x2, y1),
            (x1, y2), (x2, y2)
        ]
        
        for x, y in points:
            painter.drawEllipse(QPoint(int(x), int(y)), 5, 5)
        
        painter.setPen(old_pen)
    
    def draw_center_lines(self, painter, width, height):
        """Dibuja líneas centrales (cruz)"""
        # Línea vertical central
        painter.drawLine(int(width / 2), 0, int(width / 2), height)
        
        # Línea horizontal central
        painter.drawLine(0, int(height / 2), width, int(height / 2))
        
        # Punto central
        old_pen = painter.pen()
        painter.setPen(QPen(self.guide_color, self.line_width * 4))
        painter.drawEllipse(QPoint(int(width / 2), int(height / 2)), 6, 6)
        painter.setPen(old_pen)
    
    def draw_diagonals(self, painter, width, height):
        """Dibuja líneas diagonales"""
        # Diagonal principal (esquina superior izquierda a inferior derecha)
        painter.drawLine(0, 0, width, height)
        
        # Diagonal secundaria (esquina superior derecha a inferior izquierda)
        painter.drawLine(width, 0, 0, height)
    
    def draw_golden_spiral(self, painter, width, height):
        """Dibuja cuadrados de Fibonacci (espiral áurea)"""
        
        # Secuencia de Fibonacci
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        
        # Calcular el tamaño base y la unidad de escala
        size = min(width, height)
        unit = size / fib[-1]  # 89 es el último número
        
        # Posición inicial (centrado verticalmente, alineado a la izquierda)
        start_x = 0
        start_y = (height - size) / 2
        
        # Guardar el estilo de línea actual
        old_pen = painter.pen()
        painter.setPen(QPen(self.guide_color, self.line_width // 2))
        
        # Definir las coordenadas fijas de cada cuadrado en la espiral
        # Formato: (número_fibonacci, x_offset, y_offset)
        # Los offsets son en unidades de Fibonacci, se multiplicarán por 'unit'
        
        squares = [
            # Cuadrado 89: Esquina superior izquierda (base)
            (89, 0, 0),
            
            # Cuadrado 55: A la derecha del 89
            (55, 89, 0),
            
            # Cuadrado 34: Debajo del 55, alineado a la derecha
            (34, 89+55-34, 55),
            
            # Cuadrado 21: A la izquierda del 34, debajo del 89
            (21, 89, 55+13),
            
            # Cuadrado 13: Arriba del 21, a la izquierda
            (13, 89, 55),
            
            # Cuadrado 8: A la derecha del 13
            (8, 89+ 13, 55),
            
            # Cuadrado 5: Arriba del 8
            (5, 89+3+13, 55+8),
            
            # Cuadrado 3: A la izquierda del 5
            (3, 89+13, 55+8+2),
            
            # Cuadrado 2: Debajo del 3
            (2, 89+13, 55+8),

            #Cuadro 1: Arriba del 2 se supone
            (1,89+13+2,55+9),

            #Cuaddro 1: A la derecha del 1
            (1,89+13+2,55+8),
        ]
        
        # Dibujar cada cuadrado en su posición fija
        for side_fib, offset_x, offset_y in squares:
            side = side_fib * unit
            # Aplicar el desplazamiento horizontal de la espiral
            x = start_x + (offset_x + self.spiral_offset_x) * unit
            y = start_y + offset_y * unit
            painter.drawRect(int(x), int(y), int(side), int(side))
        
        # ===== CURVA DE LA ESPIRAL =====
        # Cada arco es 1/4 de círculo que conecta la esquina de un cuadrado con la esquina del siguiente
        # Formato: (radio_fib, centro_x_offset, centro_y_offset, ángulo_inicio, ángulo_extensión)
        # Los ángulos en Qt: 0° = derecha (3 o'clock), 90° = arriba (12 o'clock)
        # Los ángulos se especifican en 1/16 de grado (por eso se multiplican por 16)
        
        # Configurar un grosor ligeramente mayor para la curva
        painter.setPen(QPen(self.guide_color, self.line_width))
        
        spiral_arcs = [
            # Arco 1: De esquina inferior izquierda del 89 → esquina superior derecha del 55
            # Centro: esquina inferior derecha del cuadrado 89 en posición (89, 89)
            # Radio = 89 unidades
            # Desde la izquierda (180°) hacia arriba (90°) = -90° (sentido antihorario)
            (89, 89, 89, 180*16, -90*16),
            
            # Arco 2: De esquina superior izquierda del 55 → esquina inferior derecha del 34
            # Cuadrado 55 está en (89, 0), cuadrado 34 está en (110, 55)
            # Centro: esquina superior derecha del 55 en posición (89+55, 55)
            # Radio = 55 unidades
            # Desde arriba (90°) hacia la derecha (0°) = -90° (sentido antihorario)
            (55, 89, 55, 90*16, -90*16),
            
            # Arco 3: De esquina superior derecha del 34 → esquina inferior izquierda del 21
            # Cuadrado 34 está en (110, 55), cuadrado 21 está en (89, 68)
            # Centro: esquina superior izquierda del 34 en posición (110, 55)
            # Radio = 34 unidades
            # Desde la derecha (0°) hacia abajo (270°) = -90° (sentido antihorario)
            (34, 110, 55, 0*16, -90*16),
            
            # Arco 4: De esquina inferior derecha del 21 → esquina superior izquierda del 13
            # Cuadrado 21 está en (89, 68), cuadrado 13 está en (89, 55)
            # Centro: esquina inferior izquierda del 21 en posición (89, 68+21=89)
            # Radio = 21 unidades
            # Desde abajo (270°) hacia la izquierda (180°) = -90° (sentido antihorario)
            (21, 89+21, 55+13, 270*16, -90*16),
            
            # Arco 5: De esquina inferior izquierda del 13 → esquina superior derecha del 8
            # Cuadrado 13 está en (89, 55), cuadrado 8 está en (102, 55)
            # Centro: esquina inferior derecha del 13 en posición (89+13=102, 55+13=68)
            # Radio = 13 unidades
            # Desde la izquierda (180°) hacia arriba (90°) = -90° (sentido antihorario)
            (13, 102, 68, 180*16, -90*16),
            
            # Arco 6: De esquina superior izquierda del 8 → esquina inferior derecha del 5
            # Cuadrado 8 está en (102, 55), cuadrado 5 está en (105, 63)
            # Centro: esquina superior derecha del 8 en posición (102+8=110, 55+8=63)
            # Radio = 8 unidades
            # Desde arriba (90°) hacia la derecha (0°) = -90° (sentido antihorario)
            (8, 89+13, 63, 90*16, -90*16),
            
            # Arco 7: De esquina superior derecha del 5 → esquina inferior izquierda del 3
            # Cuadrado 5 está en (105, 63), cuadrado 3 está en (102, 65)
            # Centro: esquina superior izquierda del 5 en posición (105, 63)
            # Radio = 5 unidades
            # Desde la derecha (0°) hacia abajo (270°) = -90° (sentido antihorario)
            (5, 105, 63, 0*16, -90*16),
            
            # Arco 8: De esquina inferior derecha del 3 → esquina superior izquierda del 2
            # Cuadrado 3 está en (102, 65), cuadrado 2 está en (102, 63)
            # Centro: esquina inferior izquierda del 3 en posición (102, 65+3=68)
            # Radio = 3 unidades
            # Desde abajo (270°) hacia la izquierda (180°) = -90° (sentido antihorario)
            (3, 89+13+3, 55+10, 270*16, -90*16),

            # Arco 9: esquina inferior izquierda del 2 → esquina superior izquierda del 1
            # Cuadrado 2 está en (102, 63), cuadrado 1 está en (102, 60)
            # Centro: esquina inferior izquierda del 2 en posición (102, 63+3=66)
            # Radio = 3 unidades
            # Desde abajo (270°) hacia la izquierda (180°) = -90° (sentido antihorario)
            (2, 89+13+2, 55+8+2, 180*16, -90*16),

            # Arco 10: esquina inferior izquierda del 1 → esquina superior izquierda del 0
            # Cuadrado 1 está en (102, 60), cuadrado 0 está en (102, 58)
            # Centro: esquina inferior izquierda del 1 en posición (102, 60+3=63)
            # Radio = 3 unidades
            # Desde abajo (270°) hacia la izquierda (180°) = -90° (sentido antihorario)
            (1, 89+13+2, 55+8+1, 90*16, -90*16),

            # Arco 11: esquina inferior izquierda del 1 → esquina superior izquierda del 0
            # Cuadrado 1 está en (102, 60), cuadrado 0 está en (102, 58)
            # Centro: esquina inferior izquierda del 1 en posición (102, 60+3=63)
            # Radio = 3 unidades
            # Desde abajo (270°) hacia la izquierda (180°) = -90° (sentido antihorario)
            (1, 89+13+2, 55+8+1, 0*16, -90*16),
        ]
        
        # Dibujar cada arco de la espiral
        for radius_fib, center_x_offset, center_y_offset, start_angle, span_angle in spiral_arcs:
            radius = radius_fib * unit
            # Aplicar el desplazamiento horizontal de la espiral
            center_x = start_x + (center_x_offset + self.spiral_offset_x) * unit
            center_y = start_y + center_y_offset * unit
            
            # drawArc necesita un rectángulo que contenga el círculo
            # El rectángulo va desde (centro - radio) hasta (centro + radio)
            rect_x = center_x - radius
            rect_y = center_y - radius
            rect_size = radius * 2
            
            painter.drawArc(
                int(rect_x), int(rect_y), 
                int(rect_size), int(rect_size),
                start_angle, span_angle
            )
        
        # Restaurar el estilo de línea original
        painter.setPen(old_pen)
    
    def draw_grid(self, painter, width, height, rows, cols):
        """Dibuja un grid personalizado"""
        # Líneas verticales
        for i in range(1, cols):
            x = int(i * width / cols)
            painter.drawLine(x, 0, x, height)
        
        # Líneas horizontales
        for i in range(1, rows):
            y = int(i * height / rows)
            painter.drawLine(0, y, width, y)
    
    def draw_safe_areas(self, painter, width, height):
        """Dibuja áreas seguras (útil para video)"""
        # Action safe: 90% del área
        action_margin_w = int(width * 0.05)
        action_margin_h = int(height * 0.05)
        
        # Title safe: 80% del área
        title_margin_w = int(width * 0.1)
        title_margin_h = int(height * 0.1)
        
        old_pen = painter.pen()
        
        # Action safe (línea sólida)
        painter.setPen(QPen(QColor(255, 200, 0, 150), self.line_width))
        painter.drawRect(action_margin_w, action_margin_h,
                        width - 2 * action_margin_w,
                        height - 2 * action_margin_h)
        
        # Title safe (línea punteada)
        painter.setPen(QPen(QColor(255, 100, 0, 150), self.line_width, Qt.DashLine))
        painter.drawRect(title_margin_w, title_margin_h,
                        width - 2 * title_margin_w,
                        height - 2 * title_margin_h)
        
        painter.setPen(old_pen)
    
    def toggle_guide(self, guide_name):
        """Activa/desactiva una guía"""
        if guide_name in self.guides:
            self.guides[guide_name] = not self.guides[guide_name]
            self.update()
    
    def set_guide_color(self, color):
        """Establece el color de las guías"""
        self.guide_color = color
        self.update()
    
    def set_line_width(self, width):
        """Establece el grosor de las líneas"""
        self.line_width = width
        self.update()
    
    def set_opacity(self, opacity):
        """Establece la opacidad general"""
        self.window_opacity = opacity
        alpha = int(255 * opacity)
        self.guide_color.setAlpha(alpha)
        self.update()
    
    def set_spiral_offset(self, offset):
        """Establece el desplazamiento horizontal de la espiral (0-14)"""
        self.spiral_offset_x = offset
        self.update()
    
    def enable_click_through(self, enabled):
        """Habilita/deshabilita clic a través"""
        self.setAttribute(Qt.WA_TransparentForMouseEvents, enabled)
    
    def show_context_menu(self, position):
        """Muestra menú contextual"""
        menu = QMenu(self)
        
        # Opciones de guías
        guides_menu = menu.addMenu("Guías")
        
        for guide_name, guide_label in [
            ('rule_of_thirds', 'Regla de Tercios'),
            ('golden_ratio', 'Proporción Áurea'),
            ('center_lines', 'Líneas Centrales'),
            ('diagonals', 'Diagonales'),
            ('golden_spiral', 'Espiral Áurea'),
            ('grid_4x4', 'Grid 4×4'),
            ('grid_5x5', 'Grid 5×5'),
            ('safe_areas', 'Áreas Seguras')
        ]:
            action = QAction(guide_label, self)
            action.setCheckable(True)
            action.setChecked(self.guides[guide_name])
            action.triggered.connect(lambda checked, g=guide_name: self.toggle_guide(g))
            guides_menu.addAction(action)
        
        menu.addSeparator()
        
        # Opción de cerrar
        close_action = QAction("Cerrar Overlay", self)
        close_action.triggered.connect(self.hide)
        menu.addAction(close_action)
        
        menu.exec_(self.mapToGlobal(position))
