# ============================================================
# fourier_poly_validation.py
#
# Modelo:
# Tendencia polinómica + Fourier automático
# Ciclos obtenidos desde fourier_analysis.py
# Calibración último punto conocido
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

from config_legacy  import (
    CUTOFF_DATE,
    FORECAST_DAYS,
    POLY_DEGREE,
    NUMBER_OF_CYCLES,
    TRAIN_DAYS,
    FOURIER_WEIGHT,
    ERROR_FOURIER_CYCLES
)

from fourier_analysis import get_dominant_cycles

# ============================================================
# CONFIGURACIÓN
# ============================================================

CSV_FILE = "data/processed/btc_1d.csv"
DATE_COLUMN = "OpenTime"
PRICE_COLUMN = "Close"

# ============================================================
# CARGAR DATOS
# ============================================================

print("Cargando datos...")

df = pd.read_csv(CSV_FILE)
df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
df = df.sort_values(DATE_COLUMN).reset_index(drop=True)

# ============================================================
# TRAIN / TEST
# ============================================================

cutoff = pd.Timestamp(CUTOFF_DATE)
start_train = cutoff - timedelta(days=TRAIN_DAYS)

train = df[(df[DATE_COLUMN] >= start_train) & (df[DATE_COLUMN] < cutoff)].copy()
test = df[(df[DATE_COLUMN] >= cutoff) &
          (df[DATE_COLUMN] < cutoff + pd.Timedelta(days=FORECAST_DAYS))].copy()

y_train = train[PRICE_COLUMN].values

# ============================================================
# CONFIGURACIÓN MODELO
# ============================================================

print("\n" + "="*40)
print("CONFIGURACIÓN MODELO")
print("="*40)
print("Grado polinómico:", POLY_DEGREE)

# ============================================================
# OBTENER CICLOS FFT
# ============================================================

CYCLES = get_dominant_cycles(y_train, degree=POLY_DEGREE, n_cycles=NUMBER_OF_CYCLES)

print("\nCiclos Fourier:")
for c in CYCLES:
    print(" ", c, "días")

# ============================================================
# DATOS
# ============================================================

print("\n" + "="*40)
print("DATOS")
print("="*40)
print("Entrenamiento:", len(train))
print("Validación:", len(test))
print("Train desde:", train[DATE_COLUMN].min())
print("Train hasta:", train[DATE_COLUMN].max())
print("Test desde:", test[DATE_COLUMN].min())
print("Test hasta:", test[DATE_COLUMN].max())

# ============================================================
# ENTRENAMIENTO POLINOMIO
# ============================================================

n = len(y_train)
t_train = np.arange(n)
x_train = t_train / n

poly_coef = np.polyfit(x_train, y_train, POLY_DEGREE)
trend_train = np.polyval(poly_coef, x_train)
residual = y_train - trend_train

# ============================================================
# ENTRENAMIENTO FOURIER
# ============================================================

components = []
for period in CYCLES:
    freq = 1 / period
    sin = np.sin(2*np.pi*freq*t_train)
    cos = np.cos(2*np.pi*freq*t_train)
    X = np.column_stack([sin, cos])
    coef, _, _, _ = np.linalg.lstsq(X, residual, rcond=None)
    components.append({"period": period, "sin": coef[0], "cos": coef[1]})

# ============================================================
# MODELO
# ============================================================

def model_predict(length, offset_index, calibration=0):
    t = np.arange(offset_index, offset_index + length)
    x = t / n
    trend = np.polyval(poly_coef, x)
    result = np.zeros(length)
    for c in components:
        freq = 1 / c["period"]
        result += (c["sin"] * np.sin(2*np.pi*freq*t) +
                   c["cos"] * np.cos(2*np.pi*freq*t))
    #return trend + result + calibration
    return trend + (FOURIER_WEIGHT * result) + calibration
# ============================================================
# MÉTRICAS ENTRENAMIENTO
# ============================================================

model_train = model_predict(
    len(y_train),
    0,
    0
)

rmse_train = np.sqrt(
    np.mean(
        (y_train - model_train)**2
    )
)

mae_train = np.mean(
    np.abs(y_train - model_train)
)

corr_train = np.corrcoef(
    y_train,
    model_train
)[0,1]


print("\n" + "="*40)
print("MÉTRICAS ENTRENAMIENTO")
print("="*40)
print(f"Correlación : {corr_train:.6f}")
print(f"RMSE        : {rmse_train:,.2f}")
print(f"MAE         : {mae_train:,.2f}")

# ============================================================
# ESTADÍSTICAS DEL ERROR
# ============================================================

error = y_train - model_train
error_pct = 100 * error / y_train

sigma = np.std(error)
bias = np.mean(error)

print("\n" + "="*40)
print("ESTADÍSTICAS DEL ERROR")
print("="*40)

print(f"Bias                : {error.mean():,.2f}")
print(f"Mediana             : {np.median(error):,.2f}")
print(f"Desv. estándar      : {np.std(error):,.2f}")
print(f"Mínimo              : {np.min(error):,.2f}")
print(f"Máximo              : {np.max(error):,.2f}")

print(f"P5                  : {np.percentile(error,5):,.2f}")
print(f"P25                 : {np.percentile(error,25):,.2f}")
print(f"P50                 : {np.percentile(error,50):,.2f}")
print(f"P75                 : {np.percentile(error,75):,.2f}")
print(f"P95                 : {np.percentile(error,95):,.2f}")

# ============================================================
# ERROR PORCENTUAL
# ============================================================

mae_pct = np.mean(np.abs(error_pct))
rmse_pct = np.sqrt(np.mean(error_pct**2))

print("\n" + "="*40)
print("ERROR PORCENTUAL")
print("="*40)

print(f"Bias (%)            : {error_pct.mean():.3f}%")
print(f"Mediana (%)         : {np.median(error_pct):.3f}%")
print(f"Desv. estándar (%)  : {np.std(error_pct):.3f}%")
print(f"MAE (%)             : {mae_pct:.3f}%")
print(f"RMSE (%)            : {rmse_pct:.3f}%")

print(f"P5 (%)              : {np.percentile(error_pct,5):.3f}%")
print(f"P25 (%)             : {np.percentile(error_pct,25):.3f}%")
print(f"P50 (%)             : {np.percentile(error_pct,50):.3f}%")
print(f"P75 (%)             : {np.percentile(error_pct,75):.3f}%")
print(f"P95 (%)             : {np.percentile(error_pct,95):.3f}%")

# ============================================================
# CALIBRACIÓN ÚLTIMO PUNTO
# ============================================================

last_model = model_predict(1, n-1, 0)[0]
last_real = y_train[-1]
offset = last_real - last_model

print("\n" + "="*40)
print("CALIBRACIÓN")
print("="*40)
print("Modelo último día:", last_model)
print("Precio real último día:", last_real)
print("Offset aplicado:", offset)

# ============================================================
# POSICIÓN DEL ÚLTIMO ERROR EN LA CAMPANA
# ============================================================

last_error = y_train[-1] - model_train[-1]

z_score = (last_error - bias) / sigma

print("\n" + "="*40)
print("POSICIÓN ÚLTIMO ERROR")
print("="*40)

print(f"Último error : {last_error:,.2f} USD")
print(f"Bias         : {bias:,.2f} USD")
print(f"Sigma        : {sigma:,.2f} USD")
print(f"Z-score      : {z_score:.3f} σ")

# ============================================================
# BÚSQUEDA DE CORRECCIÓN ESTADÍSTICA
# ============================================================

print("\n" + "="*40)
print("CORRECCIÓN DENTRO DE LA CAMPANA")
print("="*40)

correcciones_sigma = np.arange(-2, 2.01, 0.25)

mejor_correccion = None
menor_distancia = float("inf")

for z in correcciones_sigma:

    correccion = z * sigma

    error_corregido = last_error - correccion

    distancia_bias = abs(error_corregido - bias)

    print(
        f"{z:+.2f}σ | "
        f"Ajuste: {correccion:,.2f} USD | "
        f"Error restante: {error_corregido:,.2f} USD"
    )

    if distancia_bias < menor_distancia:
        menor_distancia = distancia_bias
        mejor_correccion = correccion
        mejor_z = z


print("\nMejor corrección encontrada:")
print(f"Zona: {mejor_z:+.2f}σ")
print(f"Ajuste: {mejor_correccion:,.2f} USD")

# ============================================================
# AJUSTE ESTADÍSTICO FINAL
# ============================================================

offset_estadistico = mejor_correccion

print("\n" + "="*40)
print("AJUSTE FINAL PRONÓSTICO")
print("="*40)
print(f"Calibración último punto : {offset:,.2f} USD")
print(f"Corrección estadística  : {offset_estadistico:,.2f} USD")
print(f"Offset total futuro     : {offset + offset_estadistico:,.2f} USD")

# ============================================================
# PREDICCIÓN
# ============================================================

forecast_A = model_predict(
    len(test),
    n,
    offset
)

forecast_B = model_predict(
    len(test),
    n,
    mejor_correccion
)

real = test[PRICE_COLUMN].values

# ============================================================
# MÉTRICAS POR HORIZONTE
# ============================================================

print("\n" + "="*40)
print("MÉTRICAS POR HORIZONTE")
print("="*40)

for days in [7, 14, 18, 21, 30]:

    r = real[:days]

    fA = forecast_A[:days]
    fB = forecast_B[:days]

    corr_A = np.corrcoef(r, fA)[0,1]
    rmse_A = np.sqrt(np.mean((r-fA)**2))
    mae_A = np.mean(np.abs(r-fA))

    corr_B = np.corrcoef(r, fB)[0,1]
    rmse_B = np.sqrt(np.mean((r-fB)**2))
    mae_B = np.mean(np.abs(r-fB))

    print(f"\n{days} días")

    print(
        f"A Offset              | "
        f"Corr: {corr_A:.3f} | "
        f"RMSE: {rmse_A:,.2f} | "
        f"MAE: {mae_A:,.2f}"
    )

    print(
        f"B Estadístico | "
        f"Corr: {corr_B:.3f} | "
        f"RMSE: {rmse_B:,.2f} | "
        f"MAE: {mae_B:,.2f}"
    )

# ============================================================
# VALIDACIÓN FINAL
# ============================================================

for nombre, forecast in [
    ("A Offset", forecast_A),
    ("B Estadístico", forecast_B)
]:

    corr = np.corrcoef(real, forecast)[0,1]
    rmse = np.sqrt(np.mean((real-forecast)**2))
    mae = np.mean(np.abs(real-forecast))

    print("\n" + "="*40)
    print("VALIDACIÓN FINAL", nombre)
    print("="*40)
    print(f"Correlación : {corr:.6f}")
    print(f"RMSE        : {rmse:,.2f}")
    print(f"MAE         : {mae:,.2f}")

# ============================================================
# PENDIENTE
# ============================================================

print("\n" + "="*40)
print("ANÁLISIS DE PENDIENTE")
print("="*40)

real_change = real[-1] - real[0]

change_A = forecast_A[-1] - forecast_A[0]
change_B = forecast_B[-1] - forecast_B[0]

print(f"Cambio real {FORECAST_DAYS} días        : {real_change:,.2f}")

print(f"Modelo A Offset                         : {change_A:,.2f}")
print(f"Diferencia A                            : {(change_A-real_change):,.2f}")

print(f"Modelo B Offset + Estadístico            : {change_B:,.2f}")
print(f"Diferencia B                            : {(change_B-real_change):,.2f}")

# ============================================================
# GRÁFICO
# ============================================================

# Agregar el último punto del entrenamiento
graph_dates = pd.concat(
    [
        train[[DATE_COLUMN]].tail(1),
        test[[DATE_COLUMN]]
    ],
    ignore_index=True
)

graph_real = np.concatenate((
    [y_train[-1]],
    real
))

graph_forecast_A = np.concatenate((
    [y_train[-1]], #mismo punto inicail
    forecast_A
))

graph_forecast_B = np.concatenate((
    [model_predict(1, n, mejor_correccion)[0]],
    forecast_B
))

plt.figure(figsize=(14,6))

plt.plot(
    graph_dates[DATE_COLUMN],
    graph_real,
    marker="o",
    linewidth=2,
    label="BTC Real"
)

plt.plot(
    graph_dates[DATE_COLUMN],
    graph_forecast_A,
    marker="o",
    linewidth=2,
    label="A - Offset"
)

plt.plot(
    graph_dates[DATE_COLUMN],
    graph_forecast_B,
    marker="o",
    linewidth=2,
    label="B - Estadístico"
)

plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.title("BTC Validación Fourier Automático")
plt.tight_layout()
plt.show()

# ============================================================
# GRÁFICO ENTRENAMIENTO
# ============================================================

plt.figure(figsize=(14,6))

plt.plot(train[DATE_COLUMN], y_train, label="BTC Entrenamiento", color="blue")

plt.plot(train[DATE_COLUMN], trend_train, label="Tendencia polinómica", color="orange")

plt.plot(train[DATE_COLUMN], trend_train + residual, label="Poly + Fourier (ajuste)", color="green")

plt.grid()
plt.legend()
plt.xticks(rotation=45)
plt.title("BTC Entrenamiento - Poly + Fourier")
plt.tight_layout()
plt.show()

# ============================================================
# GRÁFICO ENTRENAMIENTO REAL VS MODELO
# ============================================================

plt.figure(figsize=(14,6))


plt.plot(
    train[DATE_COLUMN],
    y_train,
    label="BTC Real",
    linewidth=2
)


plt.plot(
    train[DATE_COLUMN],
    trend_train,
    label="Tendencia polinómica",
    linewidth=2
)


plt.plot(
    train[DATE_COLUMN],
    model_train,
    label="Poly + Fourier",
    linewidth=2
)


plt.grid()

plt.legend()

plt.xticks(rotation=45)

plt.title(
    "BTC Entrenamiento - Reconstrucción Poly + Fourier"
)

plt.tight_layout()

plt.show()

# ============================================================
# ERROR DEL MODELO EN ENTRENAMIENTO
# ============================================================

error_train = y_train - model_train

print("\n" + "="*40)
print("DISPERSIÓN DEL ERROR")
print("="*40)
print(f"σ (desv. estándar): {sigma:,.2f} USD")
print(f"2σ                : {2*sigma:,.2f} USD")

plt.figure(figsize=(14,4))

plt.plot(
    train[DATE_COLUMN],
    error_train,
    label="Error"
)

plt.axhline(
    0,
    color="black",
    linewidth=1
)

# ±1σ
plt.axhline(
    sigma,
    linestyle="--",
    color="red",
    label="+1σ"
)

plt.axhline(
    -sigma,
    linestyle="--",
    color="red",
    label="-1σ"
)

# ±2σ
plt.axhline(
    2 * sigma,
    linestyle=":",
    color="orange",
    label="+2σ"
)

plt.axhline(
    -2 * sigma,
    linestyle=":",
    color="orange",
    label="-2σ"
)

plt.grid()

plt.legend()

plt.title(
    "Error BTC - Modelo Poly + Fourier"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# ERROR PORCENTUAL DEL MODELO
# ============================================================

error_pct_train = 100 * error_train / y_train

plt.figure(figsize=(14,4))

plt.plot(
    train[DATE_COLUMN],
    error_pct_train
)

plt.axhline(
    0,
    linewidth=1
)

plt.grid()

plt.title(
    "Error porcentual (%) - Modelo Poly + Fourier"
)

plt.ylabel("%")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# FFT DEL ERROR PORCENTUAL
# ============================================================

print("\n" + "="*50)
print("FFT DEL ERROR PORCENTUAL")
print("="*50)

serie = error_pct_train - np.mean(error_pct_train)

N = len(serie)

fft = np.fft.rfft(serie)

freqs = np.fft.rfftfreq(N, d=1)

power = np.abs(fft)

# eliminar frecuencia cero
freqs = freqs[1:]
power = power[1:]

periods = 1 / freqs

# ============================================================
# CICLOS DOMINANTES DEL ERROR PORCENTUAL
# ============================================================

idx = np.argsort(power)[::-1]

print()
print(f"{'Periodo(días)':>15} {'Potencia':>15}")

for i in idx[:15]:
    print(f"{periods[i]:15.1f} {power[i]:15.2f}")

# ============================================================
# FFT DEL ERROR PORCENTUAL - ESPECTRO DE POTENCIA
# ============================================================

plt.figure(figsize=(14,6))

plt.plot(periods, power)

plt.xlim(0, 1000)

plt.xlabel("Período (días)")
plt.ylabel("Potencia espectral")

plt.title("Espectro de Potencia del Error Porcentual")

plt.grid(True)

plt.tight_layout()
plt.show()

# ============================================================
# FFT2 - MODELADO DEL ERROR PORCENTUAL
# ============================================================

TOP_ERROR_CYCLES = ERROR_FOURIER_CYCLES

print("\n")
print("="*50)
print("CONFIGURACIÓN FFT2 ERROR %")
print("="*50)
print(f"Ciclos usados FFT2: {TOP_ERROR_CYCLES}")

# quitar media
serie_error = (
    error_pct_train -
    np.mean(error_pct_train)
)


N2 = len(serie_error)

t2 = np.arange(N2)


# FFT
fft2 = np.fft.rfft(
    serie_error
)


freq2 = np.fft.rfftfreq(
    N2,
    d=1
)


power2 = np.abs(
    fft2
)


# eliminar componente continua
freq2 = freq2[1:]
fft2 = fft2[1:]
power2 = power2[1:]


period2 = 1 / freq2


# ordenar ciclos
idx2 = np.argsort(
    power2
)[::-1]


print("\n")
print("="*50)
print("CICLOS DOMINANTES FFT2 ERROR %")
print("="*50)

print(
    f"{'Periodo(días)':>15} {'Potencia':>15}"
)


for i in idx2[:15]:

    print(
        f"{period2[i]:15.1f}"
        f"{power2[i]:15.2f}"
    )


# ============================================================
# RECONSTRUCCIÓN FFT2 ERROR %
# ============================================================

error_pct_fft2 = np.zeros(N2)


for i in idx2[:TOP_ERROR_CYCLES]:

    amplitud = (
        2 *
        np.abs(fft2[i]) /
        N2
    )

    fase = np.angle(
        fft2[i]
    )


    error_pct_fft2 += (
        amplitud *
        np.cos(
            2*np.pi*freq2[i]*t2 +
            fase
        )
    )

# ============================================================
# BÚSQUEDA DE DESFASE FFT2
# ============================================================

def buscar_desfase_fft2(
    error_real,
    fft_componentes,
    freq,
    idx,
    N,
    ventanas=[30,60,100,200],
    max_shift=30
):

    resultados = {}

    t = np.arange(N)

    # reconstrucciones desplazadas
    for ventana in ventanas:

        mejor_corr = -999
        mejor_shift = 0
        mejor_rmse = None


        real_window = error_real[-ventana:]


        for shift in range(-max_shift, max_shift+1):

            curva = np.zeros(N)


            for i in idx:

                amplitud = (
                    2 *
                    np.abs(fft_componentes[i]) /
                    N
                )


                fase = np.angle(
                    fft_componentes[i]
                )


                curva += (
                    amplitud *
                    np.cos(
                        2*np.pi*freq[i]*(t+shift)
                        +
                        fase
                    )
                )


            curva_window = curva[-ventana:]


            corr = np.corrcoef(
                real_window,
                curva_window
            )[0,1]


            rmse = np.sqrt(
                np.mean(
                    (
                        real_window -
                        curva_window
                    )**2
                )
            )


            if corr > mejor_corr:

                mejor_corr = corr
                mejor_shift = shift
                mejor_rmse = rmse



        resultados[ventana] = {
            "shift": mejor_shift,
            "corr": mejor_corr,
            "rmse": mejor_rmse
        }


    return resultados

# ============================================================
# EJECUTAR BÚSQUEDA DESFASE error(t)=∑Ai​cos(2πfi​(t+d)+ϕi​) el valor a buscar es d=desface
# ============================================================

resultado_shift = buscar_desfase_fft2(
    error_pct_train,
    fft2,
    freq2,
    idx2[:TOP_ERROR_CYCLES],
    N2
)


print("\n")
print("="*50)
print("OPTIMIZACIÓN DESFASE FFT2")
print("="*50)

for dias, r in resultado_shift.items():

    print(
        f"{dias} días | "
        f"Shift: {r['shift']:+d} días | "
        f"Corr: {r['corr']:.4f} | "
        f"RMSE: {r['rmse']:.3f}%"
    )

# ============================================================
# ERROR FFT2 ÚLTIMOS DÍAS 30, 60, 100, 200
# ============================================================

print("\n")
print("="*50)
print("ÚLTIMO ERROR FFT2")
print("="*50)

for days in [30,60,100,200]:

    real_last = error_pct_train[-days:]
    fft_last = error_pct_fft2[-days:]

    corr = np.corrcoef(
        real_last,
        fft_last
    )[0,1]

    rmse = np.sqrt(
        np.mean(
            (real_last-fft_last)**2
        )
    )

    print(
        f"{days} días | "
        f"Corr: {corr:.4f} | "
        f"RMSE: {rmse:.3f}%"
    )


print("\nÚltimo error real %:",
      error_pct_train[-1])

print(
    "Último error FFT2 %:",
    error_pct_fft2[-1]
)

# ============================================================
# G
# ============================================================

plt.figure(figsize=(14,5))


plt.plot(
    train[DATE_COLUMN],
    error_pct_train,
    label="Error % FFT1",
    linewidth=1
)


plt.plot(
    train[DATE_COLUMN],
    error_pct_fft2,
    label=f"FFT2 ({TOP_ERROR_CYCLES} ciclos)",
    linewidth=2
)


plt.axhline(
    0,
    linewidth=1
)


plt.grid(True)

plt.legend()

plt.title(
    "Modelado FFT2 del Error Porcentual"
)

plt.ylabel(
    "Error (%)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# C
# ============================================================

corr_fft2 = np.corrcoef(
    error_pct_train,
    error_pct_fft2
)[0,1]


rmse_fft2 = np.sqrt(
    np.mean(
        (error_pct_train-error_pct_fft2)**2
    )
)


print("\n")
print("="*50)
print("MÉTRICAS FFT2 ERROR %")
print("="*50)

print(
    f"Correlación : {corr_fft2:.6f}"
)

print(
    f"RMSE (%)    : {rmse_fft2:.3f}"
)

# ============================================================
# MODELO COMPLETO FFT1 + FFT2
# ============================================================

model_train_fft12 = model_train / (1 - error_pct_fft2 / 100)

plt.figure(figsize=(14,6))

plt.plot(
    train[DATE_COLUMN],
    y_train,
    label="BTC Real",
    linewidth=2
)

plt.plot(
    train[DATE_COLUMN],
    model_train,
    label="FFT1",
    linewidth=2
)

plt.plot(
    train[DATE_COLUMN],
    model_train_fft12,
    label="FFT1 + FFT2",
    linewidth=2
)

plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.title("Reconstrucción completa FFT1 + FFT2")
plt.tight_layout()
plt.show()

# ============================================================
# E
# ============================================================

error_pct_fft12 = 100 * (y_train - model_train_fft12) / y_train

rmse_pct_fft12 = np.sqrt(np.mean(error_pct_fft12**2))

print(f"RMSE (%)    : {rmse_pct_fft12:.3f}")

# ============================================================
# M
# ============================================================
corr_fft12 = np.corrcoef(
    y_train,
    model_train_fft12
)[0,1]

rmse_fft12 = np.sqrt(
    np.mean(
        (y_train-model_train_fft12)**2
    )
)

mae_fft12 = np.mean(
    np.abs(
        y_train-model_train_fft12
    )
)

print("\n")
print("="*50)
print("MÉTRICAS FFT1 + FFT2")
print("="*50)
print(f"Correlación : {corr_fft12:.6f}")
print(f"RMSE        : {rmse_fft12:,.2f}")
print(f"MAE         : {mae_fft12:,.2f}")

# ============================================================
# ERROR FINAL FFT1 + FFT2
# ============================================================

error_fft12 = y_train - model_train_fft12

plt.figure(figsize=(14,4))

plt.plot(
    train[DATE_COLUMN],
    error_fft12,
    label="Error FFT1 + FFT2"
)

plt.axhline(
    0,
    color="black",
    linewidth=1
)

sigma_fft12 = np.std(error_fft12)

plt.axhline(
    sigma_fft12,
    linestyle="--",
    color="red",
    label="+1σ"
)

plt.axhline(
    -sigma_fft12,
    linestyle="--",
    color="red",
    label="-1σ"
)

plt.axhline(
    2*sigma_fft12,
    linestyle=":",
    color="orange",
    label="+2σ"
)

plt.axhline(
    -2*sigma_fft12,
    linestyle=":",
    color="orange",
    label="-2σ"
)

plt.grid(True)
plt.legend()
plt.title("Error FFT1 + FFT2")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ============================================================
# ERROR PORCENTUAL FFT1 + FFT2
# ============================================================

error_pct_fft12 = 100 * error_fft12 / y_train

plt.figure(figsize=(14,4))

plt.plot(
    train[DATE_COLUMN],
    error_pct_fft12,
    label="Error % FFT1 + FFT2"
)

plt.axhline(
    0,
    color="black",
    linewidth=1
)

plt.grid(True)
plt.legend()

plt.title("Error porcentual FFT1 + FFT2")

plt.ylabel("%")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# ESTADISTICAS
# ============================================================
print("\n")
print("="*50)
print("ESTADÍSTICAS FFT1 + FFT2")
print("="*50)

print(f"Bias (%)           : {error_pct_fft12.mean():.4f}")
print(f"Desv. estándar (%) : {np.std(error_pct_fft12):.4f}")
print(f"MAE (%)            : {np.mean(np.abs(error_pct_fft12)):.4f}")
print(f"RMSE (%)           : {np.sqrt(np.mean(error_pct_fft12**2)):.4f}")

# ============================================================
# c
# ============================================================
print("\nComparación")

print(f"RMSE FFT1       : {rmse_train:,.2f}")
print(f"RMSE FFT1+FFT2  : {rmse_fft12:,.2f}")

print(f"RMSE % FFT1     : {rmse_pct:.3f}")
print(f"RMSE % FFT1+FFT2: {rmse_pct_fft12:.3f}")

# ============================================================
# PRONÓSTICO FUTURO FFT1 + FFT2 (1040 días)
# ============================================================

print("\n")
print("="*60)
print("PRONÓSTICO FUTURO FFT1 + FFT2")
print("="*60)

FUTURE_DAYS = 77 #1040 dias 

# usar el desfase de la ventana que prefieras
SHIFT_FUTURE = resultado_shift[200]["shift"]

print(f"Horizonte : {FUTURE_DAYS} días")
print(f"Shift FFT2: {SHIFT_FUTURE:+d} días")

# ------------------------------------------------------------
# FECHAS FUTURAS
# ------------------------------------------------------------

future_dates = pd.date_range(
    start=train[DATE_COLUMN].iloc[-1] + pd.Timedelta(days=1),
    periods=FUTURE_DAYS,
    freq="D"
)

# ------------------------------------------------------------
# FFT1
# ------------------------------------------------------------

forecast_fft1 = model_predict(
    FUTURE_DAYS,
    n,
    0
)

# ------------------------------------------------------------
# FFT2 FUTURO (SIN DESFASE)
# ------------------------------------------------------------

t_future = np.arange(n, n + FUTURE_DAYS)

error_future = np.zeros(FUTURE_DAYS)

for i in idx2[:TOP_ERROR_CYCLES]:

    amplitud = (
        2 *
        np.abs(fft2[i]) /
        N2
    )

    fase = np.angle(
        fft2[i]
    )

    error_future += (
        amplitud *
        np.cos(
            2*np.pi*freq2[i]*t_future +
            fase
        )
    )

# ------------------------------------------------------------
# FFT2 FUTURO (CON DESFASE)
# ------------------------------------------------------------

error_future_shift = np.zeros(FUTURE_DAYS)

for i in idx2[:TOP_ERROR_CYCLES]:

    amplitud = (
        2 *
        np.abs(fft2[i]) /
        N2
    )

    fase = np.angle(
        fft2[i]
    )

    error_future_shift += (
        amplitud *
        np.cos(
            2*np.pi*freq2[i]*
            (t_future + SHIFT_FUTURE)
            +
            fase
        )
    )

# ------------------------------------------------------------
# MODELOS
# ------------------------------------------------------------

forecast_fft12 = forecast_fft1 / (
    1 - error_future / 100
)

forecast_fft12_shift = forecast_fft1 / (
    1 - error_future_shift / 100
)

# ------------------------------------------------------------
# GRÁFICO
# ------------------------------------------------------------

plt.figure(figsize=(16,7))

plt.plot(
    future_dates,
    forecast_fft1,
    linewidth=2,
    label="FFT1"
)

plt.plot(
    future_dates,
    forecast_fft12,
    linewidth=2,
    label="FFT1 + FFT2"
)

plt.plot(
    future_dates,
    forecast_fft12_shift,
    linewidth=2,
    label=f"FFT1 + FFT2 (Shift {SHIFT_FUTURE:+d})"
)

plt.grid(True)

plt.legend()

plt.title(
    f"Pronóstico BTC {FUTURE_DAYS} días\nFFT1 vs FFT2"
)

plt.ylabel("Precio")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
