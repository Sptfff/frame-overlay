# Guía Rápida - Composition Overlay

## ✅ Estado de Instalación

**Dependencias verificadas e instaladas:**
- ✅ PyQt5 (5.15.10)
- ✅ PyInstaller (6.3.0)
- ✅ Python 3.10.11

## 🚀 Inicio Rápido

### Ejecutar Ahora
```bash
python main.py
```

### Crear Ejecutable
```bash
build_exe.bat
```
El .exe estará en: `dist\CompositionOverlay.exe`

## 🎨 Guías Disponibles

| Guía | Uso Principal | Tecla Rápida |
|------|---------------|--------------|
| 📐 Regla de Tercios | Fotografía general | Menú contextual |
| ✨ Proporción Áurea | Fotografía artística | Menú contextual |
| 🌀 Espiral Áurea | Composición dinámica | Menú contextual |
| ➕ Líneas Centrales | Simetría | Menú contextual |
| 📏 Diagonales | Composición dinámica | Menú contextual |
| ▦ Grid 4×4 | Diseño web/gráfico | Menú contextual |
| ▦ Grid 5×5 | Diseño detallado | Menú contextual |
| 📺 Áreas Seguras | Video/broadcast | Menú contextual |

## 🎯 Controles

### Panel de Control
- **Checkboxes**: Activa/desactiva guías individuales
- **Selector de Color**: Cambia color de las guías
- **Grosor**: Ajusta de 1 a 10 pixeles
- **Opacidad**: 0-100% de transparencia
- **Clic a través**: Permite interactuar con ventanas debajo
- **Presets**: Configuraciones predefinidas

### Overlay (Clic derecho)
- Activar/desactivar guías rápidamente
- Cerrar overlay

## 💡 Tips de Uso

### Para Fotografía
1. Usa **Regla de Tercios** para fotos generales
2. **Proporción Áurea** + **Espiral Áurea** para retratos
3. **Líneas Centrales** para fotos simétricas

### Para Video
1. Activa **Áreas Seguras** (Action/Title safe)
2. Combina con **Líneas Centrales** para encuadre
3. Ajusta opacidad para no interferir con la grabación

### Para Diseño
1. **Grid 4×4** o **5×5** para layouts precisos
2. **Diagonales** para composición dinámica
3. **Proporción Áurea** para diseño armónico

### Configuración Recomendada
- **Color**: Blanco para fondos oscuros, Negro para fondos claros
- **Grosor**: 2-3px para uso general
- **Opacidad**: 70-80% para buena visibilidad sin molestar

## 🔧 Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| No veo el overlay | Verifica que "Mostrar Overlay" esté activo |
| No veo las líneas | Activa al menos una guía, aumenta opacidad |
| No puedo hacer clic en otras ventanas | Desactiva "Clic a través" |
| Las líneas son muy gruesas/finas | Ajusta el control de grosor |
| El color no contrasta | Cambia el color de las guías |

## 📝 Archivos del Proyecto

```
Overlay/
├── main.py              # Inicio de la aplicación ⭐
├── overlay_window.py    # Lógica del overlay y guías
├── control_panel.py     # Panel de control
├── requirements.txt     # Dependencias Python
├── build_exe.bat       # Crear ejecutable Windows
├── presets.json        # Configuraciones guardadas (auto-generado)
├── README.md           # Documentación completa
└── QUICKSTART.md       # Esta guía ⭐
```

## 🎓 Ejemplos de Presets

### Preset "Fotografía - Tercios"
- ✅ Regla de Tercios
- Mejor para: Paisajes, retratos, fotos generales

### Preset "Fotografía - Áureo"
- ✅ Proporción Áurea
- ✅ Espiral Áurea
- Mejor para: Retratos artísticos, composición avanzada

### Preset "Video - Safe Areas"
- ✅ Áreas Seguras
- ✅ Líneas Centrales
- Mejor para: Producción de video, broadcast

### Preset "Diseño - Grid 4×4"
- ✅ Grid 4×4
- Mejor para: Diseño web, UI/UX

## ⚡ Comandos Rápidos

### Ejecutar aplicación:
```bash
python main.py
```

### Verificar dependencias:
```bash
pip list
```

### Reinstalar dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

### Crear ejecutable:
```bash
build_exe.bat
```

## 🎉 ¡Listo para Usar!

Tu aplicación está **100% funcional** y lista para usar. Tienes dos opciones:

1. **Desarrollo**: `python main.py`
2. **Producción**: Ejecuta `build_exe.bat` para crear el .exe

**¡Disfruta creando composiciones perfectas!** 📸✨
