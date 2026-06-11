# Decision Support System (DSS) Penentuan Juara Lomba Berbasis Graf Bercabang

Aplikasi *Decision Support System* (DSS) atau Sistem Pendukung Keputusan interaktif berbasis web yang dibangun menggunakan **Python** dan **Streamlit**. Aplikasi ini dirancang untuk membantu juri dalam menentukan pemenang lomba secara objektif, dinamis, dan transparan menggunakan struktur data **Multi-Layer Directed Graph Berorientasi Cabang (Multi-Path Layered Graph)** dan **Algoritma Dijkstra**.

---

## Anggota Kelompok
* **Malvaraina Nursalim** - (NIM: 2501010084)
* **Pande Putu Vidya Reswara** - (NIM: 2501010064)
* **Kadek Satya Giri Sardhula** - (NIM: 2501010088)

---

## Fitur Utama Aplikasi
* **Dual Input Mode:** Juri dapat memasukkan data secara fleksibel, baik mengetik manual satu per satu lewat form interaktif atau mengunggah data massal secara instan via file `.csv`.
* **Multi-Path Decision Graph:** Struktur graf canggih yang membagi kriteria penilaian (*Public Speaking, Kreativitas, Penampilan*) ke dalam 3 cabang tingkatan kompetensi (`Excel`, `Good`, `Avg`).
* **AI Smart Feedback:** Modul analitik pintar yang secara otomatis mendeteksi kelemahan skor peserta dan memberikan saran evaluasi personal yang akurat.
* **Interactive Graph Visualization:** Visualisasi struktur diagram graf horizontal multi-jalur secara *real-time* menggunakan pustaka NetworkX dan Matplotlib.
* **Export Data Result:** Hasil keputusan akhir tabel peringkat juara dapat diunduh langsung ke dalam bentuk file Excel/CSV.

---

## Tech Stack & Libraries
* **Language:** Python 3
* **Interface & Web Framework:** Streamlit
* **Graph Structure & Analytics:** NetworkX
* **Data Visualization:** Matplotlib
* **Data Manipulation:** Pandas & Heapq (Min-Priority Queue)

---

## Arsitektur Model Graf Bercabang

Sistem ini memetakan alur penilaian ke dalam 11 node keputusan. Jalur yang tidak sesuai dengan kualifikasi nilai riil peserta akan diblokir oleh sistem menggunakan penalti beban ekstrem sebesar `999.0`, sehingga Algoritma Dijkstra dipaksa hanya mencari rute optimal (*Shortest Path*) dari `Start` ke `Finish` melewati cabang kompetensi asli peserta.

```text
                                  +-----------------+         +-----------------+         +-----------------+
                                  |  Public_Excel   | ------> |  Kreatif_Excel  | ------> |  Tampil_Excel   |
                                  +-----------------+ \       +-----------------+ \       +-----------------+ \
                                     ^     ^     ^     \         ^     ^     ^     \         ^     ^     ^     \
                                    /      |      \     \       /      |      \     \       /      |      \     \
                                   /       |       \     \     /       |       \     \     /       |       \     \
+-----------+                     /        |        \     v   /        |        \     v   /        |        \     v +------------+
|   Start   | ----------------->  |   Public_Good   | ------> |  Kreatif_Good   | ------> |   Tampil_Good   | ----> |   Finish   |
+-----------+                     \        |        /     ^   \        |        /     ^   \        |        /     ^ +------------+
                                   \       |       /     /     \       |       /     /     \       |       /     /
                                    \      |      /     /       \      |      /     /       \      |      /     /
                                     v     v     v     /         v     v     v     /         v     v     v     /
                                  +-----------------+         +-----------------+         +-----------------+
                                  |   Public_Avg    | ------> |   Kreatif_Avg   | ------> |   Tampil_Avg    |
                                  +-----------------+         +-----------------+         +-----------------+
```
## Cara Menjalankan Aplikasi di Lokal (CMD)
Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer/laptop Anda:

### Clone Repository

**Bash**
git clone [https://github.com/username-kamu/nama-repo-kamu.git](https://github.com/username-kamu/nama-repo-kamu.git)
cd nama-repo-kamu
Buat dan Aktifkan Virtual Environment (Disarankan)

**DOS**
python -m venv env
env\Scripts\activate
Instal Dependencies (Library)

**DOS**
pip install streamlit networkx matplotlib pandas
Jalankan Aplikasi Streamlit

**DOS**
streamlit run app.py

>>Catatan untuk Input CSV
Jika menggunakan metode input berkas, pastikan format judul kolom (header) di file Microsoft Excel/CSV Anda ditulis menggunakan huruf kecil semua seperti contoh berikut:
**Plaintext**
nama,public,kreativitas,penampilan
Peserta_A,85,90,75
Peserta_B,70,65,80
