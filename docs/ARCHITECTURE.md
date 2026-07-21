# FFTN_BTC_1D Architecture

Versión: 0.6.0

Estado: Fundación de arquitectura de referencia

---

# 1. Propósito del proyecto

FFTN_BTC_1D es un proyecto de investigación y desarrollo orientado
al análisis de series temporales de Bitcoin utilizando métodos
basados en el dominio de frecuencia.

El proyecto estudia:

- Modelado de tendencia polinómica
- Análisis Fourier
- Detección de ciclos dominantes
- Modelado del error
- Validación de pronósticos
- Reproducibilidad experimental

La arquitectura separa claramente:

- Investigación experimental
- Implementación modular
- Validación reproducible

---

# 2. Principios de arquitectura

## 2.1 Reproducibilidad

Todo experimento debe conservar:

- Definición del conjunto de datos
- Parámetros de configuración
- Parámetros del modelo
- Resultados de validación
- Referencias generadas

Un resultado sin configuración asociada no se considera
reproducible.

---

## 2.2 Separación entre investigación e implementación

El proyecto mantiene dos zonas diferentes:

reference/

Contiene modelos históricos, experimentos y referencias científicas.

src/


Contiene la implementación modular reutilizable.

El código experimental no debe reemplazar directamente
los módulos principales.

---

## 2.3 Evolución controlada

Cualquier cambio de arquitectura requiere:

1. Actualizar este documento.
2. Crear un commit en Git.
3. Registrar el cambio en la versión correspondiente.

Este documento es la referencia oficial de estructura del proyecto.

---

# 3. Estructura vigente del repositorio

Estado del repositorio después de la definición de arquitectura v0.6.0:

FFTN_BTC_1D/

├── src/
├── tests/
├── data/
│
│   └── processed/
│       └── btc_1d.csv
│
├── docs/
├── notebooks/
├── experiments/
│
└── reference/
        │
        └── legacy/
            ├── fourier_poly_validation.py
            ├── fourier_analysis.py
            ├── config_legacy.py
            └── LEGACY_NOTES.md
        │
        └── baseline/
        ├── dataset_signature.json
        └── verify_dataset.py

---

# 4. Arquitectura actual del código fuente

## src/

Contiene la implementación modular del proyecto.

Estado actual:
src/

└── fftn/

    ├── __init__.py
    │
    └── fft/

        ├── __init__.py
        ├── transform.py
        ├── spectrum.py
        └── cycles.py

Implementado en v0.5.0 como fundación del motor FFT.
---

## transform.py

Responsabilidades:

- Transformaciones Fourier
- Operaciones matemáticas FFT
- Utilidades de procesamiento de señales

---

## spectrum.py

Responsabilidades:

- Cálculo del espectro frecuencial
- Análisis de componentes de frecuencia

---

## cycles.py

Responsabilidades:

- Identificación de ciclos dominantes
- Gestión de ciclos detectados

---

# 5. Arquitectura de referencia

## 5.1 Propósito de reference/

La carpeta:

reference/


contiene elementos históricos y experimentales.

Su objetivo es:

- Preservar investigaciones anteriores
- Mantener trazabilidad científica
- Comparar futuras implementaciones
- Evitar pérdida de conocimiento experimental

No representa código productivo.

---

# 5.2 Modelo Legacy

Ubicación:

reference/

    └── legacy/
        ├── fourier_poly_validation.py
        ├── fourier_analysis.py
        ├── config_legacy.py
        └── LEGACY_NOTES.md


---

## fourier_poly_validation.py

Este archivo representa el modelo experimental original
desarrollado antes de la arquitectura modular FFTN_BTC_1D.

Componentes incluidos:

- Tendencia polinómica
- Selección automática de ciclos Fourier
- Reconstrucción Poly + Fourier
- Calibración del último punto conocido
- Estadísticas del error
- Error porcentual del modelo
- FFT del error porcentual
- Modelo Fourier del error (FFT2)
- Búsqueda de desfase del error
- Pronóstico futuro

Este archivo queda congelado como referencia histórica.

No debe modificarse directamente.

---

## Dependencias Legacy

El modelo legacy conserva sus propias dependencias
para garantizar reproducibilidad histórica.

Las dependencias incluidas dentro de:

reference/legacy/

son independientes de la implementación modular
ubicada en src/.

Archivos asociados:

- fourier_analysis.py
- config_legacy.py
- data/processed/btc_1d.csv (dataset histórico)

El objetivo es permitir la ejecución futura
del modelo original sin depender de cambios
en la arquitectura principal.

---

## Datos Legacy

El modelo experimental original utiliza una serie temporal diaria
de Bitcoin como fuente principal de datos.

Ubicación actual:

data/

└── processed/
    └── btc_1d.csv


Este archivo contiene la serie histórica utilizada para:

- Entrenamiento del modelo Poly + Fourier
- Detección de ciclos dominantes mediante FFT
- Validación histórica
- Pronóstico futuro


El dataset pertenece a la arquitectura principal del proyecto
y no se copia dentro de reference/legacy.


La separación permite:

- Evitar duplicación de datos
- Mantener una única fuente histórica
- Facilitar la comparación entre modelos legacy y modulares


El modelo legacy debe conservar compatibilidad con esta ubicación
para garantizar reproducibilidad.

---

# 5.3 Baseline

La carpeta:

reference/

└── baseline/

contiene las referencias oficiales utilizadas para comparar
la evolución del proyecto y validar futuras implementaciones.

Los archivos dentro de baseline no contienen código ejecutable.
Representan resultados y configuraciones de referencia
generadas por modelos validados.

Cada archivo tiene una responsabilidad única.

---

## cycles_reference.json

Responsabilidad:

Conservar la referencia oficial de los ciclos dominantes
seleccionados por el modelo legacy para un dataset y una
configuración determinados.

Su objetivo es permitir la comparación entre la selección
de ciclos del modelo legacy y futuras implementaciones.

---

# 6. Estrategia de migración

La evolución del proyecto seguirá el siguiente flujo:

Modelo Legacy
    |
    v
Referencia Baseline
    |
    v
Implementación Modular
    |
    v
Framework de Validación


El modelo legacy será utilizado como referencia
hasta que la implementación modular reproduzca
su comportamiento.

---

# 7. Arquitectura objetivo

La siguiente estructura representa la evolución prevista.
Estas carpetas no existen todavía en v0.6.0 y serán creadas
solamente cuando tengan una función definida.

reference/

├── README.md
├── CHANGELOG.md
│
├── legacy/
│
├── baseline/
│
│ ├── dataset_signature.json
│ ├── cycles_reference.json
│ ├── metrics_reference.json
│ └── verify_dataset.py
│
│ ├── forecast_reference.csv
│ ├── error_fft2_reference.csv
│ └── validation_report.md
│
├── model/
│
├── error_model/
│
├── validation/
│
├── visualization/
│
└── utils/

## baseline/

La carpeta:

reference/baseline/

contiene las referencias oficiales generadas
por el modelo legacy.

Su responsabilidad es conservar el estado
experimental reproducible del modelo de referencia.

Archivos actuales:

### dataset_signature.json

Responsabilidad:

- Identificar el dataset utilizado.
- Registrar características estructurales.
- Verificar integridad mediante SHA256.


### cycles_reference.json

Responsabilidad:

- Registrar los ciclos Fourier dominantes
  seleccionados por el modelo legacy.
- Asociar los ciclos con una configuración
  y dataset determinados.


### metrics_reference.json

Responsabilidad:

- Registrar métricas obtenidas durante la ejecución
  del modelo legacy.

Incluye:

- Métricas de entrenamiento.
- Métricas de validación.
- Estadísticas del error.
- Métricas FFT2.
- Métricas combinadas FFT1 + FFT2.


### verify_dataset.py

Responsabilidad:

- Verificar que el dataset actual coincide
  con la firma SHA256 registrada.
- Garantizar reproducibilidad del experimento.

Estas carpetas serán creadas únicamente cuando exista
una definición clara de su responsabilidad y contenido.

---

# 8. Reglas de arquitectura

1. Esta estructura no debe modificarse sin actualizar
   este documento.

2. Toda nueva propuesta de arquitectura debe compararse
   contra la arquitectura vigente.

3. Si una nueva estructura es aprobada, esta versión será
   reemplazada y registrada.

4. Las versiones anteriores deben quedar documentadas
   mediante CHANGELOG.md.

5. El código experimental debe permanecer separado del
   código modular.

6. Ningún modelo nuevo sustituye al modelo de referencia
   sin validación documentada.

---

# 9. Historial de versiones

## v0.5.0

Commit:
7ce5e83 - Create FFT engine foundation

Implementado:

- Fundación del motor FFT
- Estructura inicial del paquete FFT
- Análisis de espectro
- Análisis de ciclos
- Pruebas iniciales

---

## v0.6.0

Estado:

Fundación de arquitectura de referencia.

Introducido:

- Preservación del modelo legacy
- Carpeta reference/
- Dependencias históricas aisladas
- Documentación de arquitectura
- Separación entre investigación e implementación

---
## v0.6.2

Estado:

Mantenimiento de arquitectura de referencia.

Introducido:

- Carpeta reference/baseline/
- Firma de integridad SHA256 del dataset
- Verificación automática del dataset
- Referencia oficial de ciclos dominantes
- Referencia oficial de métricas del modelo legacy
- Documentación de responsabilidades baseline

Objetivo:

Fortalecer la reproducibilidad del modelo legacy
sin modificar el comportamiento del código congelado.

---

# Fin del documento
