import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config_legacy import CUTOFF_DATE, POLY_DEGREE, MAX_CYCLES, TRAIN_DAYS


# ============================================================
# CONFIGURACIÓN
# ============================================================

CSV_FILE = "data/processed/btc_1d.csv"



# ============================================================
# FUNCIÓN PRINCIPAL FFT
# ============================================================

def get_dominant_cycles(
        price,
        degree=4,
        n_cycles=8,
        show=False
):


    """
    Calcula ciclos dominantes usando FFT
    después de eliminar tendencia polinómica.

    Parámetros:
        price:
            array de precios

        degree:
            grado de tendencia polinómica

        n_cycles:
            cantidad de ciclos a devolver

        show:
            muestra gráfico FFT

    Retorna:
        lista de periodos en días
    """



    # índice temporal

    t = np.arange(
        len(price)
    )



    # ========================================================
    # QUITAR TENDENCIA POLINÓMICA
    # ========================================================

    coef = np.polyfit(
        t,
        price,
        degree
    )


    trend = np.polyval(
        coef,
        t
    )


    residual = price - trend



    # ========================================================
    # FFT
    # ========================================================

    fft = np.fft.fft(
        residual
    )


    freq = np.fft.fftfreq(
        len(residual),
        d=1
    )



    # solamente frecuencias positivas

    mask = freq > 0


    freq = freq[mask]

    power = np.abs(
        fft[mask]
    )



    # frecuencia a periodo

    periods = 1 / freq



    # ordenar por potencia

    idx = np.argsort(
        power
    )[::-1]



    cycles = []


    for i in idx[:n_cycles]:

        cycles.append(
            round(
                periods[i],
                1
            )
        )



    # ========================================================
    # GRAFICO OPCIONAL
    # ========================================================

    if show:


        plt.figure(
            figsize=(12,5)
        )


        plt.plot(
            periods[idx],
            power[idx]
        )


        plt.xscale(
            "log"
        )


        plt.xlabel(
            "Periodo (días)"
        )


        plt.ylabel(
            "Potencia"
        )


        plt.title(
            f"FFT BTC - Tendencia grado {degree}"
        )


        plt.grid(
            True
        )


        plt.show()



    return cycles




# ============================================================
# CARGAR CSV
# ============================================================

def load_price_data(
        csv_file=CSV_FILE,
        cutoff=None
):


    df = pd.read_csv(
        csv_file
    )


    df["OpenTime"] = pd.to_datetime(
        df["OpenTime"]
    )


    df = df.sort_values(
        "OpenTime"
    )



    if cutoff is not None:

        df = df[
            df["OpenTime"] <
            pd.Timestamp(cutoff)
        ]



    price = df["Close"].values.astype(float)


    return df, price




# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":



    df, price = load_price_data(
        cutoff=CUTOFF_DATE
    )



    print("="*50)
    print("DATOS FFT")
    print("="*50)


    print(
        "Inicio:",
        df["OpenTime"].min()
    )


    print(
        "Fin:",
        df["OpenTime"].max()
    )


    print(
        "Días:",
        len(price)
    )



    for degree in range(1,6):


        print()
        print("="*50)
        print(
            "GRADO:",
            degree
        )
        print("="*50)



        cycles = get_dominant_cycles(
            price,
            degree=degree,
            n_cycles=MAX_CYCLES
        )


        for c in cycles:

            print(
                c,
                "días"
            )



    # gráfico ejemplo

    get_dominant_cycles(
        price,
        degree=POLY_DEGREE,
        n_cycles=MAX_CYCLES,
        show=True
    )