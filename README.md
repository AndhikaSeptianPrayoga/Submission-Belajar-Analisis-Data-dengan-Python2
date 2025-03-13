# 📊 **Bike Rental Data Dashboard**

## 📌 **Deskripsi Proyek**

Dashboard ini dikembangkan menggunakan **Streamlit** untuk menyajikan analisis data penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, hari dalam seminggu, dan waktu dalam sehari. Tujuan utama dari dashboard ini adalah menyediakan visualisasi interaktif yang mempermudah pemahaman terhadap tren penggunaan sepeda berdasarkan data yang tersedia.

## 🛠️ **Teknologi yang Digunakan**

- **Python** – Bahasa pemrograman utama  
- **Streamlit** – Untuk membangun antarmuka dashboard yang interaktif  
- **Pandas** – Untuk pemrosesan dan manipulasi data  
- **Matplotlib & Seaborn** – Untuk keperluan visualisasi data

## 📁 **Struktur Direktori Proyek**

```
submission/
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── logo.png
├── month.png
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 **Cara Menjalankan Dashboard Secara Lokal**

### 1️⃣ Instalasi Dependensi

Pastikan Python telah terinstal pada sistem Anda. Kemudian, jalankan perintah berikut untuk menginstal seluruh dependensi yang dibutuhkan:

```sh
cd dashboard
pip install -r requirements.txt
```

### 2️⃣ Menjalankan Aplikasi Dashboard

Untuk menjalankan dashboard, gunakan perintah berikut:

```sh
streamlit run dashboard.py
```

Aplikasi akan terbuka secara otomatis di browser default Anda.

## 🔍 **Fitur Utama Dashboard**

- ✅ **Filter Rentang Tanggal**  
  Memungkinkan pengguna memilih periode waktu tertentu untuk menampilkan data yang relevan.

- ✅ **Tampilan Data (Preview Dataset)**  
  Menyajikan data harian dan per jam dalam bentuk tabel.

- ✅ **Statistik Deskriptif**  
  Menyediakan ringkasan statistik untuk data penyewaan sepeda.

- ✅ **Visualisasi Interaktif**  
  Dashboard ini menyediakan berbagai grafik untuk menganalisis tren, di antaranya:
  - Distribusi jumlah penyewaan sepeda.
  - Tren penyewaan berdasarkan waktu.
  - Pengaruh musim terhadap penggunaan sepeda.
  - Pola penyewaan berdasarkan jam dalam sehari.
  - Analisis faktor-faktor yang memengaruhi tingkat penyewaan sepeda.

## 📈 **Demo Aplikasi Dashboard**

Untuk melihat versi live dari dashboard ini, silakan kunjungi:

🔗 **[Bike Rental Dashboard – Streamlit App](https://ckxyamyrmethkqrds6zrmh.streamlit.app/)**

## 👨‍💻 **Kontributor**

- **Andhika Septian Prayoga**
