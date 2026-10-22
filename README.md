# 🖱️ Bot Auto Klik Terjadwal (Single, Multi-Klik, Multi-Jadwal & Config)

Bot klik otomatis (*Auto Clicker*) berbasis Python yang berjalan melalui Command Prompt (CMD) / Terminal. Program ini dirancang untuk mengeklik satu atau banyak titik koordinat di layar secara otomatis pada jam-jam yang telah ditentukan—sangat cocok untuk menekan tombol **Continue** saat batas waktu (*limit*) selesai, mengotomatisasi tugas aplikasi berulang, dan menjadwalkan rangkaian klik tanpa perlu ditunggu di depan layar.

---

## ✨ Fitur Utama

1. **Mode 1 Kali Klik (Single Click):** Menjadwalkan 1 kali klik pada jam tertentu.
2. **Mode Multi-Klik (Berantai):** Menjadwalkan banyak titik klik secara berurutan lengkap dengan jeda waktu (*delay*) kustom antar-klik dalam hitungan **detik (`d`)**, **menit (`m`)**, maupun **jam (`j`)**.
3. **Mode Multi-Jadwal & Multi-Klik:** Mengatur banyak sesi jam sekaligus dalam satu kali jalan (contoh: Jam `13:00` melakukan 3 klik, lanjut Jam `17:30` melakukan 2 klik, dan Jam `21:30` melakukan 4 klik).
4. **Sistem Penyimpanan Config (`config_bot.json`):** Menyimpan titik koordinat favorit (seperti tombol *Continue* atau rangkaian klik rutin) secara permanen. Saat ingin dipakai lagi, cukup pilih nama *Config* dan masukkan jam eksekusinya.
5. **3 Metode Penentuan Koordinat (X & Y):**
   * **Otomatis:** Cukup arahkan kursor mouse ke tombol target dan tunggu 5 detik.
   * **Manual:** Ketik langsung angka koordinat sumbu X dan Y jika sudah hafal.
   * **Ambil dari Config:** Memuat koordinat dari preset yang sudah pernah disimpan.
6. **Menu Cek Posisi X & Y (View Only):** Memantau koordinat kursor mouse secara *real-time* tanpa melakukan klik, dilengkapi fitur tombol `[SPASI]` untuk mencatat koordinat di layar.
7. **Hitung Mundur *Real-Time* & Verifikasi Visual:** Menampilkan sisa waktu (*countdown*) secara *live* serta menggerakkan kursor otomatis saat pengaturan awal untuk memastikan titik klik 100% tepat sasaran.

---

## 🛠️ Persiapan & Cara Install (Untuk Pemula)

Ikuti langkah-langkah berikut jika Anda baru pertama kali menggunakan program Python:

### 1. Install Python di Komputer
1. Unduh Python melalui situs resminya di [python.org/downloads](https://www.python.org/downloads/).
2. Jalankan file installer yang sudah diunduh.
3. ⚠️ **PENTING:** Pada tampilan awal instalasi, **wajib centang kotak `"Add Python to PATH"`** di bagian bawah sebelum menekan tombol **Install Now**.

### 2. Unduh Project Ini
* Klik tombol hijau **`<> Code`** di bagian atas halaman GitHub ini, lalu pilih **`Download ZIP`**.
* Ekstrak (*Extract*) file ZIP tersebut ke dalam sebuah folder di komputer Anda (misalnya di `C:\bot-autoklik`).

### 3. Install Pustaka Pendukung (`PyAutoGUI`)
1. Buka **Command Prompt (CMD)** di Windows (tekan tombol `Win + R`, ketik `cmd`, lalu tekan **Enter**).
2. Ketik perintah berikut lalu tekan **Enter** untuk menginstal pustaka penggerak mouse otomatis:
   ```bash
   pip install pyautogui
   ```

---

## 🚀 Cara Menjalankan Bot

1. Buka folder tempat Anda menyimpan file skrip ini, lalu buka **CMD** di dalam folder tersebut *(Tips cepat: klik kolom alamat folder di File Explorer, ketik `cmd`, lalu tekan **Enter**)*.
2. Jalankan perintah berikut (sesuaikan `test4.py` dengan nama file Python Anda):
   ```bash
   python test4.py
   ```
3. Pilih menu yang tersedia dengan mengetik angka **`1`** sampai **`6`** lalu tekan **Enter**:
   ```text
   ==================================================
           BOT AUTO KLIK (COMPLETE + CONFIG)         
   ==================================================
   Pilih Mode Eksekusi:
   1. Mode 1 Kali Klik (Atur Langsung)
   2. Mode Multi-Klik (1 Jadwal Waktu, Banyak Klik)
   3. Mode Multi-Jadwal & Multi-Klik (Atur Langsung)
   4. Jalankan dari Config Tersimpan (Bisa 1 Jadwal / Multi-Jadwal)
   5. Menu Config (Buat Config Baru / Lihat / Hapus Config)
   6. Cek Posisi Sumbu X dan Y (Hanya View / Tanpa Eksekusi)
   ```

---

## 📖 Panduan Menu & Contoh Penggunaan

### 🔹 Menyimpan Tombol ke Dalam Config (Menu 5 -> Menu 4)
Jika Anda sering mengeklik tombol di posisi yang sama setiap hari, simpan posisinya terlebih dahulu agar tidak perlu mengatur ulang sumbu X dan Y:
1. Pilih **`5`** (*Menu Config*) lalu pilih **`1`** (*Buat / Simpan Config Baru*).
2. Beri nama config (contoh: `continue`).
3. Masukkan jumlah titik klik (contoh: `1` untuk satu tombol, atau `2` jika ingin klik *Continue* lalu klik tombol lain).
4. Pilih cara mengunci koordinat (**`1`** = Arahkan mouse otomatis selama 5 detik, atau **`2`** = Ketik angka X dan Y manual).
5. Setelah tersimpan, kembali ke Menu Utama dan pilih **`4`** (*Jalankan dari Config Tersimpan*). Anda tinggal memilih config `continue` dan memasukkan jam berapapun bot harus mengeklik.

### 🔹 Mengatur Banyak Jam Sekaligus / Multi-Jadwal (Menu 3 atau Menu 4)
Anda dapat menjadwalkan beberapa sesi waktu berbeda dalam satu kali pengaturan:
1. Pilih **`3`** (jika ingin atur titik baru) atau **`4`** (jika memakai Config yang sudah disimpan).
2. Masukkan jam sesi pertama (contoh: `13.00`) beserta titik kliknya.
3. Saat muncul pilihan langkah selanjutnya, ketik **`1`** (*Tambah Jadwal Jam Berikutnya*) untuk menambah sesi jam kedua (contoh: `17.30`), dan seterusnya.
4. Jika seluruh jadwal sudah dimasukkan, ketik **`2`** (*Selesaikan & Jalankan Bot Sekarang*).

### 🔹 Mengecek Koordinat Layar Tanpa Klik (Menu 6)
1. Pilih **`6`** pada Menu Utama.
2. Geser mouse Anda ke posisi mana saja di layar untuk melihat angka `X` dan `Y` secara langsung.
3. Tekan **`[SPASI]`** pada keyboard untuk menandai/mencatat angka koordinat ke baris baru di CMD.
4. Tekan **`[ENTER]`** atau **`[Q]`** untuk kembali ke Menu Utama.

---

## ⏱️ Format Penulisan Waktu & Delay

| Jenis Input | Format yang Didukung | Contoh Penulisan | Keterangan |
| :--- | :--- | :--- | :--- |
| **Jam Eksekusi** | `JJ.MM` atau `JJ:MM` | `00.40` atau `15:30` | Format 24 jam (otomatis ditambah 5 detik agar aman). |
| **Jam + Detik** | `JJ.MM.DD` atau `JJ:MM:DD` | `00.40.10` atau `15:30:00` | Mengeklik tepat pada detik yang ditentukan. |
| **Delay Detik** | Angka + `d` | `10d` | Jeda 10 detik sebelum klik berikutnya. |
| **Delay Menit** | Angka + `m` | `5m` | Jeda 5 menit sebelum klik berikutnya. |
| **Delay Jam** | Angka + `j` | `1j` atau `1j 30m` | Jeda 1 jam (atau kombinasi jam & menit). |

---

## ⚠️ Tips Penting Agar Bot Tidak Meleset

* **Jangan Geser atau *Scroll* Jendela Target:** Setelah koordinat dikunci atau saat menggunakan Config, pastikan posisi jendela aplikasi/browser yang ingin diklik tidak digeser, tidak di-*scroll*, dan tidak tertutup oleh jendela CMD.
* **Matikan Mode *Sleep* pada PC/Laptop:** Jika Anda meninggalkan bot untuk waktu yang lama (misalnya menunggu tengah malam atau pagi hari), pastikan pengaturan daya (*Power & Sleep*) di Windows diatur ke **Never** agar komputer tidak mati/tidur sebelum jadwal klik tiba.
* **Cara Menghentikan Bot Secara Paksa:** Jika Anda ingin membatalkan jadwal saat hitung mundur sedang berjalan, klik pada jendela CMD lalu tekan kombinasi tombol **`Ctrl + C`** di keyboard.
