\# FFTN\_BTC\_1D Changelog



Historial de cambios arquitectónicos y versiones estables

del proyecto FFTN\_BTC\_1D.



\---



\# v0.6.0



Fecha:

2026-07-21



Estado:



Fundación de arquitectura de referencia.



\## Introducido



\### Arquitectura



\- Creación del documento oficial ARCHITECTURE.md.

\- Definición de separación entre:

&#x20; - Investigación experimental.

&#x20; - Implementación modular.

&#x20; - Validación reproducible.



\### Modelo Legacy



Se incorpora el modelo experimental original como referencia histórica:



Ubicación:



reference/legacy/



Archivos:



\- fourier\_poly\_validation.py

\- fourier\_analysis.py

\- config\_legacy.py

\- LEGACY\_NOTES.md



Características preservadas:



\- Tendencia polinómica.

\- Reconstrucción Fourier.

\- Selección automática de ciclos.

\- Calibración del último punto conocido.

\- Análisis del error porcentual.

\- FFT del error.

\- FFT2 del error.

\- Pronóstico futuro.



\### Datos



Se establece como dataset histórico reproducible:



data/processed/



\- btc\_1d.csv





El dataset permanece separado del código legacy

para evitar duplicación y mantener una única fuente

de datos.



\### Dependencias



El modelo legacy mantiene sus propias dependencias:



\- config\_legacy.py

\- fourier\_analysis.py



No depende de módulos ubicados en src/.



\---



\# v0.5.0



Commit:



7ce5e83



Estado:



Fundación del motor FFT.



\## Introducido



\- Creación del paquete fftn.

\- Primera arquitectura modular.

\- Motor inicial de transformaciones FFT.

\- Análisis de espectro.

\- Identificación de ciclos.



Estructura creada:



src/



└── fftn/



&#x20;   └── fft/



&#x20;       ├── transform.py

&#x20;       ├── spectrum.py

&#x20;       └── cycles.py



\---



\# v0.4.0



Commit:



81bc1da



Estado:



Creación de arquitectura de datos.



\## Introducido



\- Separación inicial de datos del código.

\- Organización del almacenamiento histórico.

\- Base para reproducibilidad experimental.



\---



\# v0.3.0



Commit:



742239f



Estado:



Creación de arquitectura base del proyecto.



\## Introducido



\- Estructura inicial del repositorio.

\- Organización inicial de módulos.

\- Base del proyecto FFTN\_BTC\_1D.



\---



\# Convenciones



Las versiones mayores representan cambios

arquitectónicos importantes.



Los commits intermedios pueden existir entre versiones

sin necesidad de crear un nuevo tag.



Los tags representan estados estables del proyecto.

