# Bike Sharing Analytics

Proyek analisis data untuk mengeksplorasi pola penyewaan sepeda Capital Bikeshare di Washington D.C. berdasarkan waktu dan kondisi cuaca pada periode 2011–2012.

## Isi folder

```text
BikeSharingProject/
├── data/
│   └── hour.csv
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── notebook.ipynb
├── README.md
└── requirements.txt
```

## Pertanyaan bisnis

1. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda per jam (`cnt`) antara hari kerja dan hari nonkerja sepanjang 2011–2012, serta pada jam berapa puncak permintaan terjadi pada masing-masing jenis hari?
2. Seberapa besar perbedaan rata-rata jumlah penyewaan sepeda per jam (`cnt`) pada setiap kategori kondisi cuaca (`weathersit` 1–4) selama 2011–2012, sehingga perencanaan ketersediaan sepeda dan operasional dapat mempertimbangkan kondisi cuaca?

## Menjalankan notebook

1. Buka `notebook.ipynb` menggunakan Google Colab atau Jupyter Notebook.
2. Pastikan `hour.csv` tersedia dalam folder `data/` yang satu tingkat dengan notebook. Di Google Colab, file juga dapat diunggah ke direktori kerja sebagai `hour.csv`.
3. Jalankan seluruh cell dari awal sampai akhir.
4. Pastikan semua output dan visualisasi muncul tanpa error.

## Menjalankan dashboard secara lokal

Pastikan Python sudah terpasang. Buka terminal pada folder `BikeSharingProject`, kemudian jalankan:

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

Setelah perintah dijalankan, buka alamat lokal yang ditampilkan Streamlit di terminal (biasanya `http://localhost:8501`).

## Deployment ke Streamlit Community Cloud

1. Unggah isi folder proyek ke repository GitHub.
2. Pada Streamlit Community Cloud, pilih repository dan branch yang digunakan.
3. Isi **Main file path** dengan `dashboard/dashboard.py`.
4. Deploy aplikasi.
5. Setelah deployment berhasil, simpan URL aplikasi pada file `url.txt` untuk melengkapi submission apabila deployment digunakan.

## Catatan analisis

- Dataset merupakan data historis tahun 2011–2012, sehingga tidak menggambarkan kondisi operasional terkini.
- Kolom `cnt` merupakan total penyewaan (`casual` + `registered`).
- Outlier pada jumlah penyewaan diperiksa menggunakan aturan IQR dan dipertahankan jika konsisten dengan komponen datanya; nilai ekstrem tidak otomatis dianggap salah.
- Kategori cuaca 4 memiliki jumlah observasi sangat sedikit. Rata-ratanya perlu diinterpretasikan dengan hati-hati.
- Analisis bersifat deskriptif dan tidak digunakan untuk menyimpulkan hubungan sebab-akibat.

## Sumber data

Bike Sharing Dataset, catatan penyewaan Capital Bikeshare, Washington D.C., tahun 2011–2012. Dokumentasi dataset mencantumkan publikasi terkait: Hadi Fanaee-T dan João Gama, *Event labeling combining ensemble detectors and background knowledge*, Progress in Artificial Intelligence (2013), DOI: https://doi.org/10.1007/s13748-013-0040-3.
