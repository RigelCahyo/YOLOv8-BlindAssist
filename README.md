# YOLOv8-BlindAssist

Real-time object detection system using YOLOv8 with voice feedback to assist visually impaired users in identifying surrounding obstacles.

> Deteksi Objek Real-Time Berbasis YOLO dengan Umpan Balik Suara untuk Mendukung Mobilitas Tunanetra — sistem yang memberikan umpan balik suara (Bahasa Indonesia) untuk membantu penyandang tunanetra mengenali rintangan di sekitar trotoar.

## Deskripsi Proyek

Mobilitas mandiri merupakan tantangan besar bagi penyandang tunanetra. Alat bantu tradisional seperti tongkat putih dan anjing penuntun memiliki keterbatasan: tongkat putih hanya mendeteksi rintangan dalam jangkauan fisik, sementara anjing penuntun memerlukan pelatihan mahal dan intensif. Sensor seperti ultrasonik, inframerah, atau LiDAR juga belum cukup untuk mengenali jenis objek secara spesifik.

Proyek ini mengembangkan sistem deteksi objek berbasis algoritma YOLOv8 yang diintegrasikan dengan umpan balik suara (gTTS) untuk membantu penyandang tunanetra mengenali kondisi di sekitar mereka secara real-time. Sistem mendeteksi objek dari input kamera, lalu setiap 7 detik memberi tahu pengguna objek apa saja yang terdeteksi di depannya melalui suara berbahasa Indonesia (misal: "Didepan ada: 2 orang, 1 kursi").

Proyek ini merupakan Data Science Capstone Project, Program Studi Sains Data, Fakultas Sains dan Teknologi, Universitas Teknologi Yogyakarta (2025).

**Rumusan masalah:**

- Bagaimana implementasi sistem deteksi objek berbasis YOLO yang beroperasi *real-time* untuk mendukung mobilitas tunanetra?
- Bagaimana implementasi umpan balik intuitif (suara) agar informasi deteksi tersampaikan ke pengguna?

## Dataset

- **Sumber**: dikumpulkan dari Google dan diproses/dianotasi menggunakan platform Roboflow.
- **Jumlah kelas**: 12 kategori objek yakni orang, kursi, meja, bollard, pohon, tiang, truk, sepeda, motor, mobil, gerobak, dan zebra cross.
- **Jumlah gambar**: 100–150 gambar per kategori.
- **Preprocessing**: anotasi bounding box manual, auto-orientation, resize seragam ke 640×640 piksel, serta augmentasi (rotasi, flipping, penyesuaian pencahayaan).
- **Split data**: 70% training, 15% validation, 15% testing (dibagi otomatis oleh Roboflow).

## Metodologi

1. Memahami permasalahan (kompleksitas deteksi banyak objek + cara menyampaikan info ke pengguna tunanetra)
2. Pengumpulan data dari Google & Roboflow
3. Pengolahan dataset (anotasi, augmentasi, resize, split) menggunakan Roboflow
4. Pelatihan model deteksi objek dengan YOLOv8
5. Evaluasi model menggunakan metrik mean Average Precision (mAP)
6. Deployment: integrasi model dengan kamera + umpan balik suara real-time (gTTS)

## Model dan Evaluasi

- **Model**: YOLOv8s (pre-trained small variant, `yolov8s.pt`)
- **Parameter training**: 500 epoch, image size 640px, batch size 8, dilatih dengan GPU (`device=0`)

| Metrik | Hasil |
|---|---|
| mAP50 | 0.874 |
| mAP50-95 | 0.597 |
| Precision | 93.2% |
| Recall | 81.2% |

Performa terbaik per kelas: zebra cross (mAP50 0.995), sepeda dan motor (mAP50 ~0.995 dan 0.96). Performa lebih rendah pada mAP50-95: tiang (0.395), gerobak (0.54), kursi (0.589), dan mobil (0.501).

## Insight / Analisis

- Model sangat andal mendeteksi zebra cross, sepeda, dan motor bahkan pada threshold IoU yang lebih ketat.
- Objek seperti tiang, gerobak, kursi, dan mobil lebih sulit dideteksi dengan presisi tinggi karena kemiripan visual antar kelas (misal truk kadang salah terdeteksi sebagai mobil) atau latar belakang yang kompleks.
- Model kesulitan mendeteksi objek yang terlalu jauh dari kamera.
- Nilai confidence bervariasi antar objek; bollard dan kursi cenderung terdeteksi dengan confidence tinggi, sementara gerobak dan mobil lebih rendah.

## Teknologi yang Digunakan

- **Bahasa**: Python
- **Model/Library**: Ultralytics YOLOv8, OpenCV (cv2), gTTS (Google Text-to-Speech), pygame (pemutaran audio), Roboflow (manajemen dataset & API), Matplotlib & Seaborn (visualisasi hasil evaluasi model)
- **Tools**: Visual Studio Code

## Struktur Proyek

```
YOLOv8-BlindAssist/
│
├── README.md
├── requirements.txt
│
├── train_model.py
├── Model_pakai_gTTS.py
│
└── samples/
    ├── dataset/
    │   ├── orang_01.jpg
    │   ├── mobil_01.jpg
    │   └── zebra_cross_01.jpg
    │
    └── detections/
        ├── hasil_deteksi_01.jpg
        └── hasil_deteksi_02.jpg
```

> **Catatan**: Model hasil training (`best.pt`) dan folder `runs/` tidak disertakan di repository ini karena ukurannya besar. Latih ulang sendiri menggunakan `train_model.py`, atau minta filenya langsung ke penulis.

## Cara Menjalankan

1. Clone repository ini
```bash
   git clone https://github.com/username/YOLOv8-BlindAssist.git
   cd YOLOv8-BlindAssist
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Set API key Roboflow sebagai environment variable (bukan disimpan sebagai file, supaya tidak berisiko ikut ter-commit)
```bash
   # Windows (PowerShell)
   $env:ROBOFLOW_API_KEY="xxxx"

   # macOS/Linux
   export ROBOFLOW_API_KEY="xxxx"
```
4. Jalankan training (di sesi terminal yang sama dengan langkah 3)
```bash
   python train_model.py
```
5. Jalankan sistem deteksi real-time (pastikan kamera terhubung, dan path model di `Model_pakai_gTTS.py` sudah sesuai hasil training)
```bash
   python "Model_pakai_gTTS.py"
```
6. Tekan `q` untuk keluar dari jendela deteksi.

## Batasan

- Hanya mendeteksi 12 kategori objek statis/dinamis di area trotoar (tidak mencakup hewan, objek kecil, atau rambu lalu lintas selain zebra cross).
- Dioptimalkan untuk lingkungan perkotaan dengan trotoar standar dan belum diuji untuk lingkungan non-standar (hutan, lahan pertanian, hujan deras, kabut tebal, medan kasar, atau pencahayaan ekstrem).
- Belum menyediakan informasi arah navigasi atau jarak antara objek dan pengguna, hanya memberi tahu objek apa yang ada di depan.
- Akurasi menurun untuk objek yang letaknya jauh dari kamera, dan beberapa kategori (tiang, gerobak, kursi, mobil) memiliki tingkat kesalahan deteksi lebih tinggi.

## Catatan Keamanan & Etika Data

Repository ini tidak menyertakan kredensial API apa pun — Roboflow API key diset sebagai environment variable di sesi terminal saat menjalankan program, bukan disimpan dalam file di dalam repo. Karena proyek ini tidak menggunakan `.gitignore`, penulis memastikan secara manual bahwa file-file sensitif (API key, model hasil training, dataset penuh) tidak pernah ditambahkan ke dalam commit. Dataset yang digunakan berupa gambar objek publik di area trotoar (seperti kendaraan, pejalan kaki, pohon, tiang, dan zebra cross) yang dikumpulkan dari sumber terbuka (Google dan platform Roboflow) untuk keperluan penelitian akademik non-komersial dalam rangka Data Science Capstone Project. Selama pengoperasian sistem, frame video dari kamera diproses secara real-time dan tidak disimpan secara permanen.
