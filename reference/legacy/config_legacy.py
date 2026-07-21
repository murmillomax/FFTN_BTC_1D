# =====================================================
# CONFIGURACIÓN GENERAL BTC_AI
# =====================================================

# Símbolo de Binance
SYMBOL = "BTCUSDT"

# Intervalo de las velas
# Opciones Binance: 1m, 3m, 5m, 15m, 1h, etc.
INTERVAL = "1m"

# Cantidad de velas por descarga
# Binance permite máximo 1000 por llamada
LIMIT = 1000


# =====================================================
# HISTÓRICO
# =====================================================

START_DATE = "2026-01-01"

END_DATE = "2027-01-01"

# =====================================================
# TIEMPO
# =====================================================

# Zona horaria local
TIMEZONE = "America/La_Paz"


# =====================================================
# API BINANCE
# =====================================================

API_URL = "https://api.binance.com/api/v3/klines"


# =====================================================
# MODELO
# =====================================================

# Cuántos minutos hacia adelante queremos estudiar
LOOKAHEAD = 5


# =====================================================
# ARCHIVOS
# =====================================================

# Datos originales descargados de Binance
CSV_RAW = "data/raw/btc_1m.csv"


# Datos después de crear features
CSV_FEATURES = f"data/processed/btc_features_{LOOKAHEAD}m.csv"


# Modelo entrenado
MODEL_FILE = f"models/xgboost_{LOOKAHEAD}m.pkl"

# =====================================================
# ENTRENAMIENTO / TEST
# =====================================================

# Fecha de corte para separar train/test
CUTOFF_DATE = "2026-06-15" #primer dia de la semana lunes/No olvidar entrenaniento

# Horizonte de validación (ejemplo: 30 días)
FORECAST_DAYS = 30 # Usar defaul=30 para entrena modelos

# Grado polinómico para tendencia
POLY_DEGREE = 5 # Valor entrenado SUMAN MAXIMA

# Número de ciclos Fourier
NUMBER_OF_CYCLES = 3 # Valor entrenado SUMAN MAXIMA

# Máximo de ciclos que se pueden explorar con FFT
MAX_CYCLES = 10

# Días de entrenamiento antes del cutoff
TRAIN_DAYS = 1040 # son dos ciclos de 1040 /# Valor entrenado SUMAN MAXIMA

# ==========================================
# PESO MODELO POLY + FOURIER
# ==========================================

FOURIER_WEIGHT = 1.00 # Valor entrenado SUMAN MAXIMA

# =====================================================
# FFT2 - MODELADO DEL ERROR PORCENTUAL
# =====================================================

# Número de ciclos Fourier utilizados para reconstruir el error %
ERROR_FOURIER_CYCLES = 30