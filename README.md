# ⚽ Fantasy League Simulator

Simulador de Liga de Fútbol Fantasy — Proyecto final de **Programación
Orientada a Objetos (POO)**. Los usuarios crean equipos, fichan jugadores
y compiten según los puntos generados al simular partidos.

**Stack:** Python + FastAPI + MongoDB (Motor).

---

## Funcionalidades

- Crear/consultar/actualizar/eliminar **jugadores** (Portero, Defensa,
  Medio, Delantero).
- Crear/consultar/actualizar/eliminar **usuarios** (Cliente, Administrador).
- Crear **equipos fantasy** y fichar jugadores (mercado de fichajes).
- Registrar un **partido finalizado** → calcula automáticamente el
  rendimiento de cada jugador y actualiza los puntos de los equipos
  fantasy que lo tengan fichado.

---

## Diseño orientado a objetos

**Herencia**
```
Jugador → Portero | Defensa | Medio | Delantero
Usuarios → Cliente | Administrador
EstadisticasStrategy → EstadisticasPortero | EstadisticasDefensa | EstadisticasMedio | EstadisticasDelantero
```

**Polimorfismo:** cada posición sobreescribe `calcular_puntos()` con su
propia fórmula de puntuación (`estadisticas.calcular_puntos()`).

**Encapsulamiento:** atributos sensibles del modelo (`id`, `puntos`,
`contraseña`, `token`, estadísticas) protegidos como privados (`__atributo`)
y expuestos solo mediante métodos como `to_dict()`.

**Relaciones entre clases:** `Partido` agrega los `Rendimiento` generados;
`EquipoFantasy` agrega jugadores fichados; `Rendimiento` se compone de una
`EstadisticasStrategy`; los `Controllers` dependen de los `Repository`.

**Patrones de diseño:**

| Patrón | Ubicación | Uso |
|---|---|---|
| Singleton | `config/database.py` | Única conexión activa a MongoDB |
| Factory | `models/factory_jugador.py`, `usuario_factory.py`, `factory_estadisticas.py` | Crea el tipo correcto de jugador/usuario/estadística |
| Strategy | `models/estadisticas_strategy.py` + implementaciones | Algoritmo de puntuación intercambiable por posición |
| Observer | `models/observer.py`, `partido_notifier.py`, `controllers/*_controlador.py` | Propaga puntos a jugadores y equipos tras un partido |

---

## Estructura del proyecto

```
src/
├── run.py                  # Punto de entrada (FastAPI)
├── requirements            # Dependencias
├── static/                 # Frontend estático
└── app/
    ├── config/              # Conexión a BD (Singleton) y settings
    ├── models/              # Entidades + Factory/Strategy/Observer
    ├── controllers/         # Lógica de negocio
    ├── repository/          # Acceso a datos (MongoDB)
    └── routes/              # Endpoints FastAPI
```

---

## Requisitos

- Python 3.11+
- MongoDB (local o Atlas)

---

## Instalación y ejecución

```bash
# 1. Clonar
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>

# 2. Entorno virtual
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Dependencias
pip install -r src/requirements
```

Crear el archivo `src/.env` con la cadena de conexión a MongoDB:

```env
MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/
```

Ejecutar el servidor:

```bash
cd src
uvicorn run:app --reload
```

- App: `http://127.0.0.1:8000`
- Swagger (docs interactivas): `http://127.0.0.1:8000/docs`

---

## Documentación del código

Todas las clases, métodos y funciones cuentan con docstrings (Google Style).
Se puede generar documentación navegable con:

```bash
python -m pydoc -w app.models.jugador app.controllers.jugador_controlador
```

---

## Diagrama UML

> _Agregar aquí el diagrama de clases (herencia, patrones y relaciones)._

<!-- ![Diagrama UML](docs/diagrama_uml.png) -->

---

## Autores

- Jhostin Avendaño Herrera
- Carlos Samuel Gutierrez Olejua
- Diego Armando Ruiz Landero
