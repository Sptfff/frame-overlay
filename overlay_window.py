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
        
        # Secuencia de Fibonacci: cada número es la suma de los dos anteriores
        # 1+1=2, 1+2=3, 2+3=5, 3+5=8, 5+8=13, 8+13=21, etc.
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        
        # Calcular el tamaño base: usar el lado más pequeño de la pantalla
        # para que los cuadrados siempre quepan en pantalla
        size = min(width, height)
        
        # Calcular la unidad: dividir el tamaño total por el último número de Fibonacci
        # Esto escala todos los cuadrados proporcionalmente para que llenen la pantalla
        unit = size / fib[-1]  # fib[-1] es 89, el último número de la lista
        
        # Calcular la posición inicial (comenzar desde la derecha de la pantalla)
        if width < height:
            # Si la pantalla es vertical (más alta que ancha)
            # Colocar cuadrados en el borde derecho, centrados verticalmente
            x = width - size
            y = (height - size) / 2
        else:
            # Si la pantalla es horizontal (más ancha que alta)
            # Colocar cuadrados en el borde derecho, centrados verticalmente
            x = width - size
            y = (height - size) / 2
        
        # Guardar el estilo de línea actual para restaurarlo después
        old_pen = painter.pen()
        
        # Configurar el estilo de línea para los cuadrados:
        # - Color: el color configurado por el usuario (self.guide_color)
        # - Grosor: la mitad del grosor de línea configurado
        painter.setPen(QPen(self.guide_color, self.line_width // 2))
        
        # Iterar sobre la secuencia de Fibonacci desde el más grande al más pequeño
        # range(len(fib) - 1, 1, -1) genera: 10, 9, 8, 7, 6, 5, 4, 3, 2
        # Empezamos con el cuadrado más grande (89) y terminamos con el más pequeño (2)
        for i in range(len(fib) - 1, 1, -1):
            # Calcular el lado del cuadrado actual
            # Multiplicar el número de Fibonacci por la unidad para escalar
            side = fib[i] * unit
            
            # Dibujar el cuadrado en la posición actual (x, y)
            # int() convierte a entero para coordenadas de píxeles exactas
            painter.drawRect(int(x), int(y), int(side), int(side))
            
            # Calcular la dirección de crecimiento de la espiral
            # La espiral rota en sentido antihorario: derecha → abajo → izquierda → arriba
            # direction será 0, 1, 2, o 3 dependiendo de la iteración
            direction = (len(fib) - 1 - i) % 4
            
            # Calcular la posición del siguiente cuadrado según la dirección
            if direction == 0:
                # Dirección 0: El siguiente cuadrado va ABAJO del actual
                # Mover Y hacia abajo sumando el lado del cuadrado actual
                y = y + side
                
            elif direction == 1:
                # Dirección 1: El siguiente cuadrado va a la IZQUIERDA del actual
                # Mover X hacia la izquierda restando el lado del siguiente cuadrado
                x = x - fib[i-1] * unit
                
            elif direction == 2:
                # Dirección 2: El siguiente cuadrado va ARRIBA del actual
                # Mover Y hacia arriba restando el lado del siguiente cuadrado
                y = y - fib[i-1] * unit
                
            else:
                # Dirección 3: El siguiente cuadrado va a la DERECHA del actual
                # Mover X hacia la derecha sumando el lado del cuadrado actual
                x = x + side
        
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
