@echo off
title PPM-MONY - Finanzas Sociales
color 0A

echo ========================================
echo    PPM-MONY - Finanzas Sociales
echo ========================================
echo.

:: Verificar si streamlit está instalado
pip show streamlit > nul 2>&1
if errorlevel 1 (
    echo [!] Streamlit no está instalado.
    echo [*] Instalando dependencias...
    pip install streamlit requests pandas plotly fastapi uvicorn sqlalchemy
    echo.
)

:: Iniciar backend
echo [1/2] Iniciando servidor backend...
start "PPM-Backend" cmd /k "cd backend && uvicorn testapp:app --reload --port 8000"

:: Esperar 3 segundos
timeout /t 3 /nobreak > nul

:: Iniciar frontend
echo [2/2] Iniciando aplicacion frontend...
start "PPM-Frontend" cmd /k "cd frontend && python -m streamlit run app.py --server.port 8501"

echo.
echo ========================================
echo    APLICACION INICIADA!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo No cierres estas ventanas!
echo Presiona cualquier tecla para salir...
pause > nul