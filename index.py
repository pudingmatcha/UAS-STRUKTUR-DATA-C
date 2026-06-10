import streamlit as st
import time

st.set_page_config(page_title="Searching Visualizer", layout="wide")

st.title("🔍 Searching Algorithm Visualizer")
st.markdown("Implementasi Sequential Search dan Binary Search menggunakan Python + Streamlit")

# =========================
# INPUT DATA
# =========================

st.header("Input Data")

input_data = st.text_input(
    "Masukkan data angka dipisahkan koma",
    "12,7,25,9,30,45,18"
)

search_key = st.number_input("Masukkan angka yang dicari", value=9)

algoritma = st.selectbox(
    "Pilih Algoritma",
    ["Sequential Search", "Binary Search"]
)

speed = st.slider("Kecepatan Visualisasi", 0.1, 2.0, 0.5)

# =========================
# PARSE DATA
# =========================

try:
    data = [int(x.strip()) for x in input_data.split(",")]
except:
    st.error("Input data tidak valid")
    st.stop()

# =========================
# VISUALISASI DATA
# =========================

st.header("Data")

cols = st.columns(len(data))

for i, val in enumerate(data):
    cols[i].metric(f"Index {i}", val)

# =========================
# SEQUENTIAL SEARCH
# =========================

def sequential_search(data, key):

    visual = st.empty()
    info = st.empty()

    for i in range(len(data)):

        cols = visual.columns(len(data))

        for j, val in enumerate(data):

            if j == i:
                cols[j].success(val)
            else:
                cols[j].metric(f"{j}", val)

        info.info(f"Mengecek index {i} dengan nilai {data[i]}")

        time.sleep(speed)

        if data[i] == key:
            info.success(f"Data ditemukan pada index {i}")
            return i

    info.error("Data tidak ditemukan")
    return -1

# =========================
# BINARY SEARCH
# =========================

def binary_search(data, key):

    data = sorted(data)

    st.subheader("Data Setelah Sorting")

    cols = st.columns(len(data))

    for i, val in enumerate(data):
        cols[i].metric(f"{i}", val)

    kiri = 0
    kanan = len(data) - 1

    visual = st.empty()
    info = st.empty()

    while kiri <= kanan:

        tengah = (kiri + kanan) // 2

        cols = visual.columns(len(data))

        for i, val in enumerate(data):

            if i == tengah:
                cols[i].success(val)
            elif i >= kiri and i <= kanan:
                cols[i].warning(val)
            else:
                cols[i].metric(f"{i}", val)

        info.info(
            f"Kiri={kiri}, Tengah={tengah}, Kanan={kanan}"
        )

        time.sleep(speed)

        if data[tengah] == key:
            info.success(f"Data ditemukan pada index {tengah}")
            return tengah

        elif data[tengah] < key:
            kiri = tengah + 1

        else:
            kanan = tengah - 1

    info.error("Data tidak ditemukan")
    return -1

# =========================
# EKSEKUSI
# =========================

if st.button("▶ Jalankan Searching"):

    st.divider()

    if algoritma == "Sequential Search":

        st.header("Sequential Search")

        start = time.time()

        hasil = sequential_search(data, search_key)

        end = time.time()

        st.write(f"Waktu eksekusi: {end-start:.5f} detik")

        st.subheader("Kompleksitas")
        st.write("Best Case : O(1)")
        st.write("Average Case : O(n)")
        st.write("Worst Case : O(n)")

    else:

        st.header("Binary Search")

        start = time.time()

        hasil = binary_search(data, search_key)

        end = time.time()

        st.write(f"Waktu eksekusi: {end-start:.5f} detik")

        st.subheader("Kompleksitas")
        st.write("Best Case : O(1)")
        st.write("Average Case : O(log n)")
        st.write("Worst Case : O(log n)")

# =========================
# PENJELASAN
# =========================

st.divider()

st.header("Penjelasan Algoritma")

with st.expander("Sequential Search"):
    st.write("""
    Sequential Search bekerja dengan memeriksa data satu per satu
    dari awal hingga akhir.

    Cocok untuk:
    - Data kecil
    - Data belum terurut

    Kekurangan:
    - Lambat pada data besar
    """)

with st.expander("Binary Search"):
    st.write("""
    Binary Search bekerja dengan membagi data menjadi dua bagian.

    Syarat:
    - Data harus terurut.

    Kelebihan:
    - Sangat cepat
    - Efisien untuk data besar
    """)

# =========================
# FOOTER
# =========================

st.divider()
st.caption("Mata Kuliah Struktur Data - Sub Materi Searching")
