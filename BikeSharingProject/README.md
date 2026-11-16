# Bike Sharing Analytics 🚲

Proyek analisis data Dicoding menggunakan **Bike Sharing Dataset** untuk mempelajari pola penyewaan sepeda Capital Bikeshare di Washington D.C. pada periode 2011–2012.

## Struktur proyek

```text
BikeSharingProject/
├── dashboard/
│   ├── all_data.csv
│   └── dashboard.py
├── data/
│   ├── hour.csv
│   └── Readme.txt
├── notebook.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

`hour.csv` adalah dataset utama yang dianalisis. `data/Readme.txt` merupakan dokumentasi asli dataset. `dashboard/all_data.csv` adalah data yang telah disiapkan untuk dibaca dashboard.

## Pertanyaan bisnis

1. Bagaimana pola rata-rata jumlah penyewaan sepeda (`cnt`) berdasarkan jam dalam sehari dan status hari (hari kerja atau hari nonkerja) selama periode 2011–2012, serta pada jam berapa puncak permintaan terjadi pada masing-masing jenis hari untuk membantu pengaturan ketersediaan sepeda?
2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda (`cnt`) pada setiap kategori kondisi cuaca (`weathersit` 1–4) selama periode 2011–2012, dan kategori cuaca mana yang menunjukkan tingkat permintaan paling rendah sebagai bahan pertimbangan penyesuaian operasional?

## Menjalankan notebook

1. Buka `notebook.ipynb` menggunakan Google Colab atau Jupyter Notebook.
2. Pastikan `data/hour.csv` tersedia. Jika menggunakan Google Colab, unggah `hour.csv` ke folder `data/` atau ke direktori kerja sesuai lokasi yang dicari notebook.
3. Jalankan seluruh cell dari awal sampai akhir dan pastikan output serta grafik tampil.
4. Isi email dan ID Dicoding pada bagian identitas notebook sebelum submission.

## Menjalankan dashboard secara lokal

Pastikan Python sudah terpasang. Buka terminal pada folder utama `BikeSharingProject`, lalu jalankan:

### Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Setelah perintah dijalankan, buka alamat lokal yang ditampilkan Streamlit (umumnya `http://localhost:8501`).

## Deployment ke Streamlit Community Cloud

1. Unggah isi proyek ke repository GitHub.
2. Buat aplikasi baru di Streamlit Community Cloud dan pilih repository serta branch yang digunakan.
3. Isi **Main file path** dengan `dashboard/dashboard.py`.
4. Deploy aplikasi. Setelah berhasil, catat URL aplikasi yang sebenarnya untuk dimasukkan ke `url.txt`.

`url.txt` belum disertakan karena dashboard belum di-deploy. Jangan menggantinya dengan alamat umum Streamlit; file tersebut akan dibuat setelah URL aplikasi aktif tersedia.

## Catatan analisis

- Dataset merupakan catatan historis tahun 2011–2012, bukan kondisi operasional terkini.
- `cnt` merupakan jumlah total penyewaan, yaitu penjumlahan `casual` dan `registered`.
- Tidak ditemukan missing value atau baris duplikat pada pemeriksaan awal. Oleh karena itu, baris tidak dihapus tanpa alasan.
- Nilai ekstrem pada jumlah penyewaan tidak otomatis dianggap salah; konsistensinya diperiksa terhadap variabel penyusun.
- Kategori cuaca 4 memiliki jumlah pengamatan sangat sedikit, sehingga hasil rata-ratanya harus ditafsirkan secara hati-hati.
- Analisis bersifat deskriptif dan tidak membuktikan hubungan sebab-akibat.

## Sumber data

Bike Sharing Dataset, catatan Capital Bikeshare, Washington D.C., 2011–2012. Dokumentasi dataset mencantumkan publikasi: Hadi Fanaee-T dan João Gama, *Event labeling combining ensemble detectors and background knowledge*, Progress in Artificial Intelligence (2013), DOI: https://doi.org/10.1007/s13748-013-0040-3.
