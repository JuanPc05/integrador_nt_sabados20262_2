# Proyecto Integrador — Nuevas Tecnologías

Pipeline de datos en Python: generación con Faker, exportación (CSV/Excel/JSON),
limpieza con pandas, consultas y reporte con matplotlib.

## Requisitos previos

- **Python 3.10 o superior**
  - Windows: descárgalo de [python.org](https://www.python.org/downloads/).
    Durante la instalación **marca la casilla "Add Python to PATH"**.
  - Linux (Ubuntu): `sudo apt install python3 python3-venv`
- **Git** instalado y configurado.
- **Visual Studio Code** con la extensión oficial **Python** (Microsoft).

## 1. Clonar el repositorio

```bash
git clone <URL-del-repo>
cd <carpeta-del-repo>
```

Al clonar quedarás en la rama `develop` (es la rama por defecto). Nunca se
trabaja directo sobre `main` ni sobre `develop`: cada tarea va en su propia
rama (ver "Flujo de trabajo Git").

## 2. Crear y activar el entorno virtual (.venv)

El `.venv` es **local a tu máquina** y no se sube al repositorio.
Cada integrante crea el suyo. Ejecuta los comandos según tu sistema:

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

> **Si al activar aparece un error de "running scripts is disabled":**
> PowerShell bloquea scripts por seguridad. Habilítalos solo para tu usuario
> (una sola vez) y vuelve a intentar la activación:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Alternativa: usar la terminal **CMD** en lugar de PowerShell, con
> `.venv\Scripts\activate.bat`.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cuando esté activo, tu terminal mostrará `(.venv)` al inicio de la línea.
Para desactivarlo en cualquier SO: `deactivate`.

## 3. Instalar las dependencias

Con el `.venv` **activo**:

```bash
pip install -r requirements.txt
```

## 4. Seleccionar el intérprete en VS Code

1. Abre la carpeta del proyecto en VS Code.
2. `Ctrl+Shift+P` → escribe **Python: Select Interpreter**.
3. Elige el que apunta a la carpeta `.venv` del proyecto.

A partir de ahí, la terminal integrada activará el `.venv` automáticamente
y el autocompletado reconocerá pandas, Faker, etc.

## 5. Verificar que todo quedó bien

Con el `.venv` activo:

```bash
python -c "import pandas, faker, matplotlib, openpyxl; print('entorno OK')"
```

Si imprime `entorno OK`, el entorno está listo.

## Convenciones de código (obligatorias por ser equipo mixto Windows/Linux)

- **UTF-8 siempre.** Todo manejo de archivos lleva `encoding="utf-8"`
  explícito (`open`, `read_csv`, `to_csv`, `read_json`, ...). Evita caracteres
  corruptos con acentos y `ñ`.
- **Rutas con `pathlib`.** Construye rutas con `Path("data") / "raw" / archivo`,
  nunca concatenando `/` o `\` a mano.

## Flujo de trabajo Git (GitFlow)

- `main` y `develop` están protegidas: **no se hace push directo**.
- Toda tarea (historia de usuario) se trabaja en una rama propia creada
  desde `develop`:

```bash
git checkout develop
git pull
git checkout -b feature/PRI-3-limpieza   # ejemplo: prefijo de tabla + n° de HU
# ...trabajas y haces commits...
git push origin feature/PRI-3-limpieza
```

- Luego abres un **Pull Request** de tu rama hacia `develop` en GitHub.
- El PR requiere **1 aprobación** de un compañero antes de poder mergear.

- EQUIPO 2