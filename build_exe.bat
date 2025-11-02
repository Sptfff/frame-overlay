@echo off
echo ========================================
echo   Construyendo Composition Overlay
echo ========================================
echo.

REM Verificar que estamos en el entorno virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Entorno virtual activado
) else (
    echo Advertencia: No se encontro entorno virtual
)

echo.
echo Verificando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo   Creando ejecutable...
echo ========================================

REM Limpiar builds anteriores
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

REM Crear ejecutable con PyInstaller
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="CompositionOverlay" ^
    --add-data="presets.json;." ^
    --noconsole ^
    main.py

echo.
echo ========================================
if exist "dist\CompositionOverlay.exe" (
    echo   Exito! Ejecutable creado
    echo   Ubicacion: dist\CompositionOverlay.exe
    echo ========================================
    echo.
    echo Puedes ejecutar el programa desde:
    echo   dist\CompositionOverlay.exe
) else (
    echo   Error: No se pudo crear el ejecutable
    echo ========================================
)

echo.
pause
