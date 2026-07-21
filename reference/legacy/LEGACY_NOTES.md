# Legacy Fourier Poly Validation

## Origin

Modelo inicial desarrollado antes de la arquitectura FFTN_BTC_1D.

Este modelo representa la primera implementación experimental
del sistema Poly + Fourier utilizado para análisis y pronóstico
de series temporales BTC.

---

## Files

- fourier_poly_validation.py
- config_legacy.py
- fourier_analysis.py

---

## Dependencies

El modelo legacy conserva sus propias dependencias
para garantizar reproducibilidad histórica.

No utiliza módulos de src/.

Dataset requerido:

data/processed/btc_1d.csv


Columnas principales utilizadas:

- OpenTime
- Close

---

## Purpose

Preservar el modelo experimental original:

- Tendencia polinómica
- Fourier automático
- Calibración último punto conocido
- Estadísticas del error
- Error porcentual del modelo
- FFT del error porcentual
- FFT2 del error
- Búsqueda de desfase del error
- Pronóstico futuro

---

## Migration Verification

El modelo fue migrado desde la ubicación original
hacia:

reference/legacy/


manteniendo la lógica matemática original.

Validación realizada:

- Ejecución del modelo original.
- Ejecución del modelo dentro de FFTN_BTC_1D.
- Comparación de resultados obtenidos.

Resultado:

Las dos ejecuciones producen resultados equivalentes.

El modelo legacy queda establecido como referencia
experimental reproducible.

---

## Status

Código congelado.

No modificar directamente.

Será utilizado como referencia para la migración modular.
