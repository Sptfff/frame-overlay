# Composition Overlay

Aplicación profesional para sobreponer guías de composición fotográfica y diseño sobre cualquier contenido en pantalla.

## 🎨 Características

### Guías de Composición
- **📐 Regla de Tercios**: Grid 3×3 clásico con puntos de intersección destacados
- **✨ Proporción Áurea**: Rectángulos basados en φ (1.618)
- **🌀 Espiral Áurea**: Espiral de Fibonacci para composición dinámica
- **➕ Líneas Centrales**: Cruz central para composición simétrica
- **📏 Diagonales**: Líneas diagonales para composición dinámica
- **▦ Grids Personalizados**: 4×4 y 5×5 para diseño preciso
- **📺 Áreas Seguras**: Action safe y Title safe para producción de video

### Controles Avanzados
- 🎨 **Color personalizable** con selector de color
- 📏 **Grosor de línea ajustable** (1-10px)
- 🔲 **Control de opacidad** (0-100%)
- 🖱️ **Clic a través** - interactúa con ventanas debajo del overlay
- 💾 **Sistema de presets** - guarda y carga configuraciones
- 📋 **Menú contextual** (clic derecho)

### Presets Incluidos
1. **Fotografía - Tercios**: Para composición fotográfica clásica
2. **Fotografía - Áureo**: Proporción áurea y espiral
3. **Video - Safe Areas**: Áreas seguras para broadcast
4. **Diseño - Grid 4×4**: Para diseño web/gráfico
5. **Diseño - Grid 5×5**: Grid más denso
6. **Completo**: Todas las guías visibles

## 🚀 Instalación y Uso

### Opción 1: Ejecutar desde Python

1. **Requisitos**: Python 3.8 o superior

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar**:
   ```bash
   python main.py
   ```

### Opción 2: Crear Ejecutable (.exe)

1. **Ejecutar el script de construcción**:
   ```bash
   build_exe.bat
   ```

2. **El ejecutable estará en**: `dist\CompositionOverlay.exe`

3. **Distribuir**: Puedes copiar el .exe a cualquier carpeta

## 🎮 Cómo Usar

### Panel de Control

1. **Guías de Composición**: 
   - Marca/desmarca las guías que quieras ver
   - Combina múltiples guías según necesites

2. **Apariencia**:
   - Clic en "Seleccionar Color" para cambiar el color de las guías
   - Ajusta el grosor de línea con el selector
   - Controla la opacidad con el deslizador

3. **Opciones Avanzadas**:
   - "Clic a través": Permite interactuar con ventanas debajo del overlay
   - "Mostrar Overlay": Toggle rápido de visibilidad

4. **Presets**:
   - Selecciona un preset del menú desplegable
   - Guarda tu configuración actual con "💾 Guardar"
   - Carga configuraciones guardadas con "📂 Cargar"

### Overlay (Ventana Transparente)

- **Clic derecho**: Abre menú contextual con opciones rápidas
- El overlay se mantiene siempre al frente
- Cubre toda la pantalla (pantalla completa)

## 📋 Casos de Uso

### Fotografía
- Composición de fotos en tiempo real
- Revisar composición de videos/películas
- Análisis de obras de arte

### Diseño
- Alineación de elementos en diseño web
- Grid para diseño gráfico
- Proporciones para UI/UX

### Video
- Verificar áreas seguras antes de grabar
- Composición de tomas
- Edición de video con referencias

## 🛠️ Requisitos Técnicos

### Para ejecutar desde código:
- Windows 7 o superior
- Python 3.8+
- PyQt5 5.15.10
- PyInstaller 6.3.0 (solo para crear .exe)

### Para ejecutable:
- Windows 7 o superior
- No requiere Python instalado

## 📁 Estructura del Proyecto

```
Overlay/
├── main.py                  # Punto de entrada
├── overlay_window.py        # Ventana de overlay con guías
├── control_panel.py         # Panel de control
├── requirements.txt         # Dependencias Python
├── build_exe.bat           # Script para crear .exe
├── presets.json            # Configuraciones guardadas (generado)
└── README.md               # Este archivo
```

## 🎯 Atajos y Tips

1. **Clic derecho en overlay**: Acceso rápido a activar/desactivar guías
2. **Presets**: Usa presets para cambiar rápido entre configuraciones
3. **Clic a través**: Actívalo cuando quieras interactuar con aplicaciones debajo
4. **Múltiples guías**: Combina regla de tercios + diagonales para composición avanzada
5. **Color**: Usa blanco para fondos oscuros, negro para fondos claros

## 🐛 Solución de Problemas

**El overlay no se ve**:
- Verifica que "Mostrar Overlay" esté marcado
- Aumenta la opacidad
- Verifica que al menos una guía esté activa

**No puedo interactuar con otras ventanas**:
- Desactiva "Clic a través del overlay"
- Usa el panel de control para ajustes

**El color no se ve bien**:
- Ajusta el color según tu fondo
- Aumenta/disminuye el grosor de línea
- Ajusta la opacidad

## 📝 Notas de Desarrollo

- Desarrollado con PyQt5 para máximo rendimiento
- Overlay de pantalla completa con transparencia
- Sistema de presets basado en JSON
- Compatible con múltiples monitores

## 🔄 Próximas Características (Ideas)

- [ ] Atajos de teclado globales
- [ ] Soporte para múltiples monitores independientes
- [ ] Más guías de composición (espiral logarítmica, etc.)
- [ ] Modo "snapshot" para capturar pantalla con guías
- [ ] Temas de color predefinidos

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus proyectos.

---

**¿Preguntas o sugerencias?** ¡Disfruta creando composiciones perfectas! 📸🎨
