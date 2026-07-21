# Legacy Fourier Poly Validation

## Origin

Modelo experimental original desarrollado antes de la arquitectura modular FFTN_BTC_1D.

Este código corresponde al prototipo inicial de investigación utilizado para explorar:

- Tendencia polinómica
- Reconstrucción Fourier
- Modelado del error del modelo

## Files

- fourier_poly_validation.py
- config_legacy.py

## Dependencies (original)

El modelo original dependía de:

- config.py
- fourier_analysis.py
- data/processed/btc_1d.csv

Estas dependencias fueron conservadas como referencia histórica.

## Purpose

Preservar el modelo experimental original antes de la migración modular.

Componentes incluidos:

- Tendencia polinómica
- Selección automática de ciclos Fourier
- Reconstrucción Poly + Fourier
- Calibración del último punto conocido
- Análisis estadístico del error
- FFT del error porcentual
- Modelado Fourier del error porcentual (FFT2)
- Búsqueda de desfase del error
- Pronóstico futuro

## Status

Código congelado.

No modificar directamente.

Este directorio funciona como referencia histórica para la migración hacia la arquitectura modular FFTN_BTC_1D.