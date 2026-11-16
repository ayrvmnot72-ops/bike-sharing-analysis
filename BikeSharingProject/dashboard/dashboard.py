
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 1. KONFIGURASI DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
)

# Mengambil lokasi folder utama proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# Menggunakan dataset asli hour.csv
DATA_PATH = BASE_DIR / "data" / "hour.csv"


# =========================================================
# 2. MEMUAT DAN MENYIAPKAN DATA
# =========================================================

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Memuat dan menyiapkan dataset asli Bike Sharing."""

    data = pd.read_csv(path, parse_dates=["dteday"])

    # Informasi tahun, bulan, dan jam
    data["year"] = data["yr"].map({
        0: 2011,
        1: 2012
    })

    data["month"] = data["mnth"].astype(int)
    data["hour"] = data["hr"].astype(int)

    # Mengelompokkan jenis hari
    data["day_type"] = data["workingday"].map({
        1: "Hari kerja",
        0: "Hari nonkerja"
    })

    # Memberikan label kondisi cuaca
    weather_mapping = {
        1: "Cerah / sedikit berawan",
        2: "Berkabut / berawan",
        3: "Hujan atau salju ringan",
        4: "Cuaca ekstrem"
    }

    data["weather_label"] = data["weathersit"].map(
        weather_mapping
    )

    # Mengelompokkan jam berdasarkan periode waktu
    data["time_period"] = pd.cut(
        data["hour"],
        bins=[-1, 5, 10, 15, 18, 23],
        labels=[
            "Dini hari (00–05)",
            "Pagi (06–10)",
            "Siang (11–15)",
            "Sore (16–18)",
            "Malam (19–23)"
        ],
        include_lowest=True
    )

    return data


# =========================================================
# 3. MEMERIKSA DAN MEMUAT DATASET
# =========================================================

st.title("🚲 Bike Sharing Analytics")

st.caption(
    "Analisis pola penyewaan sepeda Capital Bikeshare, "
    "Washington D.C. berdasarkan waktu dan kondisi cuaca "
    "(2011–2012)."
)

if not DATA_PATH.exists():
    st.error(
        f"Dataset tidak ditemukan pada lokasi: {DATA_PATH}. "
        "Pastikan file hour.csv berada di folder data."
    )
    st.stop()

try:
    data = load_data(DATA_PATH)

except Exception as error:
    st.error(f"Terjadi kesalahan saat memuat dataset: {error}")
    st.stop()


# =========================================================
# 4. FILTER ANALISIS
# =========================================================

st.sidebar.header("Filter Analisis")

# Filter tahun
available_years = sorted(
    data["year"].dropna().unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Tahun",
    options=available_years,
    default=available_years
)

# Filter bulan
available_months = list(range(1, 13))

selected_months = st.sidebar.multiselect(
    "Bulan",
    options=available_months,
    default=available_months,
    format_func=lambda month: pd.Timestamp(
        2000, month, 1
    ).strftime("%B")
)

# Filter jenis hari
day_options = [
    "Hari kerja",
    "Hari nonkerja"
]

selected_day_types = st.sidebar.multiselect(
    "Jenis hari",
    options=day_options,
    default=day_options
)

# Filter kondisi cuaca
weather_options = (
    data[["weathersit", "weather_label"]]
    .drop_duplicates()
    .sort_values("weathersit")["weather_label"]
    .tolist()
)

selected_weather = st.sidebar.multiselect(
    "Kondisi cuaca",
    options=weather_options,
    default=weather_options
)

st.sidebar.caption(
    "Catatan: data merupakan catatan historis tahun "
    "2011–2012, bukan kondisi operasional terkini."
)


# =========================================================
# 5. MENERAPKAN FILTER
# =========================================================

filtered = data[
    data["year"].isin(selected_years)
    & data["month"].isin(selected_months)
    & data["day_type"].isin(selected_day_types)
    & data["weather_label"].isin(selected_weather)
].copy()

if filtered.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter yang dipilih."
    )
    st.stop()


# =========================================================
# 6. MENGHITUNG KEY METRICS
# =========================================================

total_rentals = int(filtered["cnt"].sum())

average_per_hour = filtered["cnt"].mean()

observations = len(filtered)

peak_hour = (
    filtered.groupby("hour")["cnt"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)


# =========================================================
# 7. MENAMPILKAN KEY METRICS
# =========================================================

metric_cols = st.columns(4)

metric_cols[0].metric(
    "Total penyewaan",
    f"{total_rentals:,.0f}"
)

metric_cols[1].metric(
    "Rata-rata per jam",
    f"{average_per_hour:,.1f}"
)

metric_cols[2].metric(
    "Jumlah observasi",
    f"{observations:,.0f}"
)

metric_cols[3].metric(
    "Jam dengan rata-rata tertinggi",
    f"{int(peak_hour):02d}.00"
)

st.divider()


# =========================================================
# 8. VISUALISASI POLA PENYEWAAN BERDASARKAN JAM
# =========================================================

st.subheader("1. Pola Penyewaan Berdasarkan Jam")

hourly = (
    filtered.groupby(
        ["hour", "day_type"],
        as_index=False
    )
    .agg(
        average_rentals=("cnt", "mean"),
        observation_count=("cnt", "size")
    )
)

fig_hour = px.line(
    hourly,
    x="hour",
    y="average_rentals",
    color="day_type",
    markers=True,
    hover_data={
        "observation_count": True,
        "hour": True
    },
    labels={
        "hour": "Jam",
        "average_rentals": "Rata-rata penyewaan",
        "day_type": "Jenis hari",
        "observation_count": "Jumlah observasi"
    }
)

fig_hour.update_layout(
    xaxis=dict(
        dtick=1,
        title="Jam dalam sehari"
    ),
    yaxis_title="Rata-rata penyewaan sepeda",
    legend_title_text="Jenis hari",
    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10
    )
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)


# =========================================================
# 9. VISUALISASI PENYEWAAN BERDASARKAN CUACA
# =========================================================

st.subheader(
    "2. Rata-rata Penyewaan Berdasarkan Kondisi Cuaca"
)

weather = (
    filtered.groupby(
        ["weathersit", "weather_label"],
        as_index=False
    )
    .agg(
        average_rentals=("cnt", "mean"),
        observation_count=("cnt", "size")
    )
    .sort_values("weathersit")
)

fig_weather = px.bar(
    weather,
    x="weather_label",
    y="average_rentals",
    text_auto=".1f",
    hover_data={
        "observation_count": True,
        "weathersit": True
    },
    labels={
        "weather_label": "Kondisi cuaca",
        "average_rentals": "Rata-rata penyewaan",
        "observation_count": "Jumlah observasi"
    }
)

fig_weather.update_layout(
    xaxis_title="Kondisi cuaca",
    yaxis_title="Rata-rata penyewaan per jam",
    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10
    )
)

st.plotly_chart(
    fig_weather,
    use_container_width=True
)

# Peringatan kategori cuaca dengan observasi sedikit
rare_weather = weather[
    weather["observation_count"] < 30
]

if not rare_weather.empty:

    rare_n = int(
        rare_weather["observation_count"].sum()
    )

    st.info(
        f"Perhatian: kategori cuaca dengan kurang dari "
        f"30 observasi memiliki total {rare_n} observasi "
        "pada filter saat ini. Interpretasikan rata-ratanya "
        "secara hati-hati."
    )


# =========================================================
# 10. VISUALISASI BERDASARKAN PERIODE WAKTU
# =========================================================

st.subheader(
    "3. Pola Penyewaan Berdasarkan Periode Waktu"
)

period_order = [
    "Dini hari (00–05)",
    "Pagi (06–10)",
    "Siang (11–15)",
    "Sore (16–18)",
    "Malam (19–23)"
]

period = (
    filtered.groupby(
        ["time_period", "day_type"],
        as_index=False,
        observed=True
    )
    .agg(
        average_rentals=("cnt", "mean")
    )
)

period["time_period"] = pd.Categorical(
    period["time_period"],
    categories=period_order,
    ordered=True
)

period = period.sort_values("time_period")

fig_period = px.bar(
    period,
    x="time_period",
    y="average_rentals",
    color="day_type",
    barmode="group",
    labels={
        "time_period": "Periode waktu",
        "average_rentals": "Rata-rata penyewaan",
        "day_type": "Jenis hari"
    }
)

fig_period.update_layout(
    xaxis_title="Periode waktu",
    yaxis_title="Rata-rata penyewaan per jam",
    legend_title_text="Jenis hari",
    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10
    )
)

st.plotly_chart(
    fig_period,
    use_container_width=True
)


# =========================================================
# 11. MENAMPILKAN DAN MENGUNDUH DATA HASIL FILTER
# =========================================================

with st.expander("Lihat data setelah filter"):

    st.dataframe(
        filtered.head(100),
        use_container_width=True
    )

    csv_bytes = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Unduh data hasil filter (CSV)",
        data=csv_bytes,
        file_name="bike_sharing_filtered.csv",
        mime="text/csv"
    )


# =========================================================
# 12. INFORMASI SUMBER DATA
# =========================================================

st.caption(
    "Sumber: Bike Sharing Dataset, Capital Bikeshare, "
    "Washington D.C. Data historis 2011–2012. "
    "Rata-rata menunjukkan pola deskriptif dan tidak "
    "membuktikan hubungan sebab-akibat."
)
