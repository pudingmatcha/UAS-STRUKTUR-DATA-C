import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq

st.set_page_config(page_title="DSS Penentuan Juara - Kelompok Graph", layout="wide")

st.title("Decision Support System (DSS) Penentuan Juara Lomba")
st.markdown("---")

# ========================================================
# 1. INPUT DATA PESERTA
# ========================================================
st.header("Input Data Peserta")

opsi_input = st.radio(
    "Pilih Metode Input Data:",
    ["Ketik Manual", "Upload File CSV"],
    horizontal=True
)

peserta = []

if opsi_input == "Ketik Manual":
    jumlah = st.number_input("Jumlah Peserta yang Mengikuti Lomba", min_value=2, max_value=20, value=3)

    for i in range(jumlah):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nama = st.text_input(f"Nama Peserta {i+1}", value=f"Peserta_{i+1}", key=f"nama_{i}")
        with col2:
            public = st.number_input(f"Public Speaking {nama} (0-100)", 0, 100, 80, key=f"p_{i}")
        with col3:
            kreativitas = st.number_input(f"Kreativitas {nama} (0-100)", 0, 100, 85, key=f"k_{i}")
        with col4:
            penampilan = st.number_input(f"Penampilan {nama} (0-100)", 0, 100, 75, key=f"t_{i}")

        peserta.append({
            "nama": nama, "public": public, "kreativitas": kreativitas, "penampilan": penampilan
        })
        
else:
    uploaded_file = st.file_uploader("Unggah File DATA_PESERTA.CSV kamu di sini:", type=["csv"])
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file)
        for index, row in df_input.iterrows():
            peserta.append({
                "nama": row["nama"],
                "public": int(row["public"]),
                "kreativitas": int(row["kreativitas"]),
                "penampilan": int(row["penampilan"])
            })
        st.success(f"Berhasil memuat {len(peserta)} data peserta dari file CSV!")
    else:
        st.warning("Silakan unggah file CSV terlebih dahulu untuk memproses data.")
        st.info("Format Judul Kolom CSV: nama, public, kreativitas, penampilan")
        st.stop()

# ========================================================
# 2. BOBOT KRITERIA
# ========================================================
st.markdown("---")
st.header("Pengaturan Bobot Kriteria (%)")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    b_public = st.slider("Bobot Nilai Public Speaking", 0, 100, 40)
with col_b2:
    b_kreativitas = st.slider("Bobot Nilai Kreativitas", 0, 100, 30)
with col_b3:
    b_penampilan = st.slider("Bobot Nilai Penampilan", 0, 100, 30)

if b_public + b_kreativitas + b_penampilan != 100:
    st.warning(f"Total bobot: {b_public + b_kreativitas + b_penampilan}%. Disarankan total berakumulasi 100%.")

# ========================================================
# FUNGSI HELPER: KATEGORI & COST LOGIC
# ========================================================
def hitung_cost_dan_kategori(nilai, bobot):
    penalty_dasar = 100 - nilai
    cost = round(penalty_dasar * (bobot / 100), 2)
    
    if nilai >= 85:
        return "Excel", cost
    elif nilai >= 70:
        return "Good", cost
    else:
        return "Avg", cost

# FUNGSI DIJKSTRA
def dijkstra_pencatatan_jalur(graph, start, end):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    parent = {node: None for node in graph.nodes}
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end:
            break
        if current_distance > distances[current_node]:
            continue
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return distances[end], path

# ========================================================
# PROSES PEMBENTUKAN GRAF BERCABANG PER PESERTA
# ========================================================
hasil_dss = []
graphs_peserta = {}
jalur_terpilih_peserta = {}

for p in peserta:
    G = nx.DiGraph()
    nama_p = p["nama"]
    
    # 1. Tentukan kategori riil si peserta di tiap kriteria beserta cost-nya
    kat_p, cost_p = hitung_cost_dan_kategori(p["public"], b_public)
    kat_k, cost_k = hitung_cost_dan_kategori(p["kreativitas"], b_kreativitas)
    kat_t, cost_t = hitung_cost_dan_kategori(p["penampilan"], b_penampilan)
    
    # 2. Definisikan semua kemungkinan Node di dalam sistem (Struktur Cabang)
    nodes_sistem = [
        "Start",
        "Public_Excel", "Public_Good", "Public_Avg",
        "Kreatif_Excel", "Kreatif_Good", "Kreatif_Avg",
        "Tampil_Excel", "Tampil_Good", "Tampil_Avg",
        "Finish"
    ]
    G.add_nodes_from(nodes_sistem)
    
    # 3. Hubungkan Start ke seluruh cabang Public Speaking
    G.add_edge("Start", "Public_Excel", weight=cost_p if kat_p == "Excel" else 999.0)
    G.add_edge("Start", "Public_Good", weight=cost_p if kat_p == "Good" else 999.0)
    G.add_edge("Start", "Public_Avg", weight=cost_p if kat_p == "Avg" else 999.0)
    
    # 4. Hubungkan antar cabang: Public -> Kreativitas (Ganti 'dalam' menjadi 'in')
    for cabang_sebelum in ["Excel", "Good", "Avg"]:
        G.add_edge(f"Public_{cabang_sebelum}", "Kreatif_Excel", weight=cost_k if kat_k == "Excel" else 999.0)
        G.add_edge(f"Public_{cabang_sebelum}", "Kreatif_Good", weight=cost_k if kat_k == "Good" else 999.0)
        G.add_edge(f"Public_{cabang_sebelum}", "Kreatif_Avg", weight=cost_k if kat_k == "Avg" else 999.0)
        
    # 5. Hubungkan antar cabang: Kreativitas -> Penampilan (Ganti 'dalam' menjadi 'in')
    for cabang_sebelum in ["Excel", "Good", "Avg"]:
        G.add_edge(f"Kreatif_{cabang_sebelum}", "Tampil_Excel", weight=cost_t if kat_t == "Excel" else 999.0)
        G.add_edge(f"Kreatif_{cabang_sebelum}", "Tampil_Good", weight=cost_t if kat_t == "Good" else 999.0)
        G.add_edge(f"Kreatif_{cabang_sebelum}", "Tampil_Avg", weight=cost_t if kat_t == "Avg" else 999.0)
        
    # 6. Hubungkan seluruh cabang Penampilan ke Finish (Cost 0)
    G.add_edge("Tampil_Excel", "Finish", weight=0.0)
    G.add_edge("Tampil_Good", "Finish", weight=0.0)
    G.add_edge("Tampil_Avg", "Finish", weight=0.0)
    
    graphs_peserta[nama_p] = G
    
    # Hitung Lintasan Terpendek dengan Dijkstra
    total_cost, jalur_hitung = dijkstra_pencatatan_jalur(G, "Start", "Finish")
    skor_akhir = 100 - total_cost
    
    jalur_bersih = [n for n in jalur_hitung]
    jalur_terpilih_peserta[nama_p] = jalur_bersih
    
    hasil_dss.append({
        "Peserta": nama_p,
        "Total Penalty (Cost)": round(total_cost, 2),
        "Skor Akhir Rekomendasi": round(skor_akhir, 2),
        "Jalur Evaluasi Graph": " -> ".join(jalur_bersih),
        "p_val": p["public"], "k_val": p["kreativitas"], "t_val": p["penampilan"]
    })

df = pd.DataFrame(hasil_dss)
df = df.sort_values(by="Skor Akhir Rekomendasi", ascending=False).reset_index(drop=True)
df.index += 1
df.index.name = 'Ranking'

# ========================================================
# 3. DISPLAY OUTPUT UTAMA
# ========================================================
st.markdown("---")
st.header("Hasil Rekomendasi Juara")
st.dataframe(df[["Peserta", "Skor Akhir Rekomendasi", "Total Penalty (Cost)"]], use_container_width=True)

juara_1 = df.iloc[0]["Peserta"]
skor_juara = df.iloc[0]["Skor Akhir Rekomendasi"]
st.success(f" **Rekomendasi Utama Juara 1 jatuh kepada:** {juara_1} dengan Akumulasi Skor Akhir **{skor_juara}**")

# AI SMART FEEDBACK
st.subheader("🤖 AI Smart Feedback & Analisis Evaluasi")
for index, row in df.iterrows():
    nama_p = row["Peserta"]
    if index == 1:
        st.info(f" **{nama_p} (Juara 1):** Luar biasa! Mampu mempertahankan rute terbaik dengan menembus cabang kompetensi tertinggi.")
    else:
        nilai_min = min(row["p_val"], row["k_val"], row["t_val"])
        if nilai_min == row["p_val"]:
            saran = "fokus meningkatkan teknik Public Speaking."
        elif nilai_min == row["k_val"]:
            saran = "mengeksplorasi ide inovasi di aspek Kreativitas."
        else:
            saran = "memperbaiki estetika Penampilan presentasi."
        st.write(f"• **{nama_p} (Peringkat {index}):** Terhambat masuk cabang 'Excel' karena nilai rendah. Disarankan {saran}")

# ========================================================
# 4. JALUR TRACE & VISUALISASI BER-CABANG
# ========================================================
st.markdown("---")
st.header("Visualisasi Jalur Keputusan Bercabang")

st.subheader("Lintasan Jalur Sistem (Trace Dijkstra)")
st.table(df[["Peserta", "Jalur Evaluasi Graph", "Total Penalty (Cost)"]])

st.subheader("Grafik Struktur Multi-Jalur (Cabang)")
pilihan_peserta = st.selectbox("Pilih Peserta untuk Melihat Jalur yang Dilalui:", [p["nama"] for p in peserta])

if pilihan_peserta:
    graph_tampil = graphs_peserta[pilihan_peserta]
    jalur_aktif = jalur_terpilih_peserta[pilihan_peserta]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    pos_bercabang = {
        "Start": (0, 0),
        "Public_Excel": (3, 1.5), "Public_Good": (3, 0), "Public_Avg": (3, -1.5),
        "Kreatif_Excel": (7, 1.5), "Kreatif_Good": (7, 0), "Kreatif_Avg": (7, -1.5),
        "Tampil_Excel": (11, 1.5), "Tampil_Good": (11, 0), "Tampil_Avg": (11, -1.5),
        "Finish": (14, 0)
    }
    
    edge_colors = []
    edge_widths = []
    
    for u, v in graph_tampil.edges():
        if u in jalur_aktif and v in jalur_aktif and jalur_aktif.index(v) == jalur_aktif.index(u) + 1:
            edge_colors.append("#2A9D8F") 
            edge_widths.append(4.0)
        else:
            edge_colors.append("#E0E0E0") 
            edge_widths.append(1.0)
            
    node_colors = ["#E76F51" if node in jalur_aktif else "#4EA8DE" for node in graph_tampil.nodes()]

    nx.draw_networkx_nodes(graph_tampil, pos_bercabang, node_size=1800, node_color=node_colors, edgecolors="#1B6CA8", ax=ax)
    nx.draw_networkx_edges(graph_tampil, pos_bercabang, arrows=True, arrowsize=18, edge_color=edge_colors, width=edge_widths, ax=ax)
    nx.draw_networkx_labels(graph_tampil, pos_bercabang, font_size=8, font_weight="bold", font_color="#102A43", ax=ax)

    labels_terpilih = {}
    for u, v in graph_tampil.edges():
        if u in jalur_aktif and v in jalur_aktif and jalur_aktif.index(v) == jalur_aktif.index(u) + 1:
            w = graph_tampil[u][v]['weight']
            labels_terpilih[(u, v)] = f"Cost: {w}"
            
    nx.draw_networkx_edge_labels(graph_tampil, pos_bercabang, edge_labels=labels_terpilih, ax=ax, font_color='#D90429', font_weight="bold", font_size=10)

    ax.set_xlim(-1, 15)
    ax.set_ylim(-2.5, 2.5)
    ax.axis("off")
    fig.tight_layout()
    st.pyplot(fig)

# Download Button CSV
csv = df[["Peserta", "Skor Akhir Rekomendasi", "Total Penalty (Cost)"]].to_csv().encode('utf-8')
st.download_button(label="Download Hasil Rekomendasi (CSV)", data=csv, file_name='hasil_dss_juara_bercabang.csv', mime='text/csv')
