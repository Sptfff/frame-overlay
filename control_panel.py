"""
Panel de Control para configurar el Overlay
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QCheckBox, QPushButton, QLabel, QSlider, 
                             QColorDialog, QComboBox, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QKeySequence
import json
import os


class ControlPanel(QWidget):
    closed = pyqtSignal()
    
    def __init__(self, overlay_window):
        super().__init__()
        self.overlay = overlay_window
        self.presets_file = "presets.json"
        
        self.init_ui()
        self.load_presets()
        
    def init_ui(self):
        """Inicializa la interfaz del panel de control"""
        self.setWindowTitle("Control de Composición")
        self.setGeometry(100, 100, 450, 700)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # Título
        title = QLabel("🎨 Composition Overlay Control")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Grupo: Guías de Composición
        guides_group = self.create_guides_group()
        main_layout.addWidget(guides_group)
        
        # Grupo: Apariencia
        appearance_group = self.create_appearance_group()
        main_layout.addWidget(appearance_group)
        
        # Grupo: Opciones Avanzadas
        advanced_group = self.create_advanced_group()
        main_layout.addWidget(advanced_group)
        
        # Grupo: Presets
        presets_group = self.create_presets_group()
        main_layout.addWidget(presets_group)
        
        # Botones principales
        buttons_layout = self.create_main_buttons()
        main_layout.addLayout(buttons_layout)
        
        # Información de atajos
        shortcuts_info = QLabel(
            "💡 Atajos: Clic derecho en overlay para menú contextual"
        )
        shortcuts_info.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        shortcuts_info.setWordWrap(True)
        main_layout.addWidget(shortcuts_info)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def create_guides_group(self):
        """Crea el grupo de guías de composición"""
        group = QGroupBox("Guías de Composición")
        layout = QVBoxLayout()
        
        self.guide_checkboxes = {}
        
        guides = [
            ('rule_of_thirds', '📐 Regla de Tercios', 'Grid 3×3 clásico'),
            ('golden_ratio', '✨ Proporción Áurea', 'Ratio φ (1.618)'),
            ('center_lines', '➕ Líneas Centrales', 'Cruz central'),
            ('diagonals', '📏 Diagonales', 'Líneas diagonales'),
            ('golden_spiral', '🌀 Espiral Áurea', 'Espiral de Fibonacci'),
            ('grid_4x4', '▦ Grid 4×4', 'Cuadrícula 4 filas × 4 columnas'),
            ('grid_5x5', '▦ Grid 5×5', 'Cuadrícula 5 filas × 5 columnas'),
            ('safe_areas', '📺 Áreas Seguras', 'Action/Title safe para video')
        ]
        
        for guide_id, label, tooltip in guides:
            checkbox = QCheckBox(label)
            checkbox.setToolTip(tooltip)
            checkbox.setChecked(self.overlay.guides[guide_id])
            checkbox.stateChanged.connect(
                lambda state, g=guide_id: self.toggle_guide(g)
            )
            self.guide_checkboxes[guide_id] = checkbox
            layout.addWidget(checkbox)
        
        # Control de desplazamiento de espiral (solo visible cuando la espiral está activa)
        spiral_offset_layout = QHBoxLayout()
        spiral_offset_label = QLabel("   ↔️ Desplazamiento Espiral:")
        self.spiral_offset_slider = QSlider(Qt.Horizontal)
        self.spiral_offset_slider.setRange(0, 14)
        self.spiral_offset_slider.setValue(0)
        self.spiral_offset_slider.valueChanged.connect(self.change_spiral_offset)
        self.spiral_offset_value_label = QLabel("0")
        spiral_offset_layout.addWidget(spiral_offset_label)
        spiral_offset_layout.addWidget(self.spiral_offset_slider)
        spiral_offset_layout.addWidget(self.spiral_offset_value_label)
        layout.addLayout(spiral_offset_layout)
        
        group.setLayout(layout)
        return group
    
    def create_appearance_group(self):
        """Crea el grupo de configuración de apariencia"""
        group = QGroupBox("Apariencia")
        layout = QVBoxLayout()
        
        # Color de las guías
        color_layout = QHBoxLayout()
        color_label = QLabel("Color de Guías:")
        self.color_button = QPushButton("Seleccionar Color")
        self.color_button.clicked.connect(self.select_color)
        self.update_color_button()
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        layout.addLayout(color_layout)
        
        # Grosor de línea
        width_layout = QHBoxLayout()
        width_label = QLabel("Grosor de Línea:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10)
        self.width_spinbox.setValue(self.overlay.line_width)
        self.width_spinbox.valueChanged.connect(self.change_line_width)
        self.width_value_label = QLabel(f"{self.overlay.line_width}px")
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spinbox)
        width_layout.addWidget(self.width_value_label)
        width_layout.addStretch()
        layout.addLayout(width_layout)
        
        # Opacidad
        opacity_layout = QVBoxLayout()
        opacity_label = QLabel("Opacidad:")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(self.overlay.window_opacity * 100))
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        self.opacity_value_label = QLabel(f"{int(self.overlay.window_opacity * 100)}%")
        
        opacity_controls = QHBoxLayout()
        opacity_controls.addWidget(self.opacity_slider)
        opacity_controls.addWidget(self.opacity_value_label)
        
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addLayout(opacity_controls)
        layout.addLayout(opacity_layout)
        
        group.setLayout(layout)
        return group
    
    def create_advanced_group(self):
        """Crea el grupo de opciones avanzadas"""
        group = QGroupBox("Opciones Avanzadas")
        layout = QVBoxLayout()
        
        # Click-through
        self.clickthrough_checkbox = QCheckBox("🖱️ Clic a través del overlay")
        self.clickthrough_checkbox.setToolTip(
            "Permite hacer clic a través del overlay hacia las ventanas debajo"
        )
        self.clickthrough_checkbox.stateChanged.connect(self.toggle_clickthrough)
        layout.addWidget(self.clickthrough_checkbox)
        
        # Visibilidad del overlay
        self.visibility_checkbox = QCheckBox("👁️ Mostrar Overlay")
        self.visibility_checkbox.setChecked(True)
        self.visibility_checkbox.stateChanged.connect(self.toggle_visibility)
        layout.addWidget(self.visibility_checkbox)
        
        group.setLayout(layout)
        return group
    
    def create_presets_group(self):
        """Crea el grupo de presets"""
        group = QGroupBox("Presets")
        layout = QVBoxLayout()
        
        # Selector de preset
        preset_layout = QHBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Fotografía - Tercios",
            "Fotografía - Áureo",
            "Video - Safe Areas",
            "Diseño - Grid 4x4",
            "Diseño - Grid 5x5",
            "Completo - Todo visible",
            "Personalizado"
        ])
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        
        preset_layout.addWidget(QLabel("Preset:"))
        preset_layout.addWidget(self.preset_combo)
        layout.addLayout(preset_layout)
        
        # Botones de preset
        preset_buttons = QHBoxLayout()
        save_preset_btn = QPushButton("💾 Guardar")
        save_preset_btn.clicked.connect(self.save_current_preset)
        save_preset_btn.setToolTip("Guarda la configuración actual")
        
        load_preset_btn = QPushButton("📂 Cargar")
        load_preset_btn.clicked.connect(self.load_preset_dialog)
        load_preset_btn.setToolTip("Carga un preset guardado")
        
        preset_buttons.addWidget(save_preset_btn)
        preset_buttons.addWidget(load_preset_btn)
        layout.addLayout(preset_buttons)
        
        group.setLayout(layout)
        return group
    
    def create_main_buttons(self):
        """Crea los botones principales"""
        layout = QHBoxLayout()
        
        # Botón toggle overlay
        self.toggle_overlay_btn = QPushButton("👁️ Ocultar Overlay")
        self.toggle_overlay_btn.clicked.connect(self.quick_toggle_overlay)
        self.toggle_overlay_btn.setStyleSheet(
            "QPushButton { padding: 10px; font-size: 14px; font-weight: bold; }"
        )
        
        # Botón cerrar
        close_btn = QPushButton("❌ Salir")
        close_btn.clicked.connect(self.close_application)
        close_btn.setStyleSheet(
            "QPushButton { padding: 10px; font-size: 14px; }"
        )
        
        layout.addWidget(self.toggle_overlay_btn)
        layout.addWidget(close_btn)
        
        return layout
    
    # Métodos de control
    
    def toggle_guide(self, guide_name):
        """Activa/desactiva una guía"""
        self.overlay.toggle_guide(guide_name)
    
    def select_color(self):
        """Abre diálogo de selección de color"""
        color = QColorDialog.getColor(self.overlay.guide_color, self)
        if color.isValid():
            self.overlay.set_guide_color(color)
            self.update_color_button()
    
    def update_color_button(self):
        """Actualiza el botón de color con el color actual"""
        color = self.overlay.guide_color
        self.color_button.setStyleSheet(
            f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); "
            f"color: {'black' if color.lightness() > 128 else 'white'};"
        )
    
    def change_line_width(self, value):
        """Cambia el grosor de las líneas"""
        self.overlay.set_line_width(value)
        self.width_value_label.setText(f"{value}px")
    
    def change_opacity(self, value):
        """Cambia la opacidad"""
        opacity = value / 100
        self.overlay.set_opacity(opacity)
        self.opacity_value_label.setText(f"{value}%")
    
    def change_spiral_offset(self, value):
        """Cambia el desplazamiento horizontal de la espiral"""
        self.overlay.set_spiral_offset(value)
        self.spiral_offset_value_label.setText(f"{value}")
    
    def toggle_clickthrough(self, state):
        """Activa/desactiva clic a través"""
        self.overlay.enable_click_through(state == Qt.Checked)
    
    def toggle_visibility(self, state):
        """Muestra/oculta el overlay"""
        if state == Qt.Checked:
            self.overlay.show()
            self.toggle_overlay_btn.setText("👁️ Ocultar Overlay")
        else:
            self.overlay.hide()
            self.toggle_overlay_btn.setText("👁️ Mostrar Overlay")
    
    def quick_toggle_overlay(self):
        """Toggle rápido del overlay"""
        self.visibility_checkbox.setChecked(not self.visibility_checkbox.isChecked())
    
    def apply_preset(self, preset_name):
        """Aplica un preset predefinido"""
        # Desactivar todas las guías primero
        for guide in self.overlay.guides:
            self.overlay.guides[guide] = False
        
        # Aplicar preset específico
        if preset_name == "Fotografía - Tercios":
            self.overlay.guides['rule_of_thirds'] = True
        elif preset_name == "Fotografía - Áureo":
            self.overlay.guides['golden_ratio'] = True
            self.overlay.guides['golden_spiral'] = True
        elif preset_name == "Video - Safe Areas":
            self.overlay.guides['safe_areas'] = True
            self.overlay.guides['center_lines'] = True
        elif preset_name == "Diseño - Grid 4x4":
            self.overlay.guides['grid_4x4'] = True
        elif preset_name == "Diseño - Grid 5x5":
            self.overlay.guides['grid_5x5'] = True
        elif preset_name == "Completo - Todo visible":
            for guide in self.overlay.guides:
                self.overlay.guides[guide] = True
        
        # Actualizar checkboxes SIN disparar eventos
        # Bloquear señales temporalmente para evitar llamadas a toggle_guide()
        for guide_id, checkbox in self.guide_checkboxes.items():
            checkbox.blockSignals(True)  # Bloquear señales
            checkbox.setChecked(self.overlay.guides[guide_id])
            checkbox.blockSignals(False)  # Desbloquear señales
        
        # Forzar actualización visual del overlay
        self.overlay.update()
    
    def save_current_preset(self):
        """Guarda la configuración actual como preset"""
        config = {
            'guides': self.overlay.guides.copy(),
            'color': {
                'r': self.overlay.guide_color.red(),
                'g': self.overlay.guide_color.green(),
                'b': self.overlay.guide_color.blue(),
                'a': self.overlay.guide_color.alpha()
            },
            'line_width': self.overlay.line_width,
            'opacity': self.overlay.window_opacity
        }
        
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(config, f, indent=2)
            QMessageBox.information(self, "Éxito", "Preset guardado correctamente")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el preset:\n{e}")
    
    def load_presets(self):
        """Carga presets desde archivo"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    config = json.load(f)
                self.apply_loaded_preset(config)
            except Exception as e:
                pass  # Silencioso si no hay preset
    
    def load_preset_dialog(self):
        """Carga un preset desde archivo"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    config = json.load(f)
                self.apply_loaded_preset(config)
                QMessageBox.information(self, "Éxito", "Preset cargado correctamente")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo cargar el preset:\n{e}")
        else:
            QMessageBox.information(self, "Info", "No hay presets guardados")
    
    def apply_loaded_preset(self, config):
        """Aplica un preset cargado"""
        # Aplicar guías
        if 'guides' in config:
            for guide_id, enabled in config['guides'].items():
                if guide_id in self.overlay.guides:
                    self.overlay.guides[guide_id] = enabled
                    if guide_id in self.guide_checkboxes:
                        # Bloquear señales para evitar disparar eventos
                        self.guide_checkboxes[guide_id].blockSignals(True)
                        self.guide_checkboxes[guide_id].setChecked(enabled)
                        self.guide_checkboxes[guide_id].blockSignals(False)
        
        # Aplicar color
        if 'color' in config:
            c = config['color']
            color = QColor(c['r'], c['g'], c['b'], c['a'])
            self.overlay.set_guide_color(color)
            self.update_color_button()
        
        # Aplicar grosor
        if 'line_width' in config:
            self.overlay.set_line_width(config['line_width'])
            # Bloquear señales del spinbox también
            self.width_spinbox.blockSignals(True)
            self.width_spinbox.setValue(config['line_width'])
            self.width_spinbox.blockSignals(False)
        
        # Aplicar opacidad
        if 'opacity' in config:
            self.overlay.set_opacity(config['opacity'])
            # Bloquear señales del slider
            self.opacity_slider.blockSignals(True)
            self.opacity_slider.setValue(int(config['opacity'] * 100))
            self.opacity_slider.blockSignals(False)
        
        self.overlay.update()
    
    def close_application(self):
        """Cierra la aplicación"""
        self.closed.emit()
        self.close()
    
    def closeEvent(self, event):
        """Evento de cierre de ventana"""
        self.closed.emit()
        event.accept()
