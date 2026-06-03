# Guia didactica de Fisica 2

Aplicacion web liviana para resolver y recalcular tres ejercicios de campo magnetico.
Usa Python + Flask dentro de Docker, sin instalar dependencias en el sistema local.

## Ejecutar con Docker

```powershell
docker compose up --build
```

Luego abrir:

```text
http://localhost:8000
```

## Ejecutar tests dentro del contenedor

```powershell
docker compose run --rm fisica2 python -m unittest discover -s tests
```

## Estructura

- `app/main.py`: rutas web y lectura de parametros editables.
- `app/physics.py`: formulas fisicas reutilizables.
- `app/templates/index.html`: pagina tipo wiki/ayuda.
- `app/static/styles.css`: estetica visual inspirada en UTN FRRE.
- `tests/test_physics.py`: pruebas de las formulas principales.

## Ejercicios incluidos

1. Campo magnetico de un conductor rectilineo infinitamente largo.
2. Campo magnetico total de dos conductores paralelos con corrientes entrantes.
7. Cantidad de vueltas de una bobina circular para producir un campo en su centro.
