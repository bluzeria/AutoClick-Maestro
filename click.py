# ==============================================================================
# Project : AutoClick-Maestro (Bot Auto Klik Multi-Jadwal & Multi-Klik)
# Author  : Bluz Tekno (https://github.com/bluzeria/AutoClick-Maestro)
# License : Copyright (c) 2026 Bluz Tekno. All Rights Reserved.
# ==============================================================================



import datetime
import json
import os
import re
import time
import pyautogui

# Pustaka bawaan Windows untuk mendeteksi tombol keyboard tanpa menghentikan layar live
try:
  import msvcrt

  HAS_MSVCRT = True
except ImportError:
  HAS_MSVCRT = False

CONFIG_FILE = "config_bot.json"


# ==================== FUNGSI DATABASE CONFIG ====================
def muat_config():
  """Memuat daftar config dari file JSON."""
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return {}
  return {}


def simpan_config(data_config):
  """Menyimpan daftar config ke file JSON agar permanen."""
  with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(data_config, f, indent=4)


# ==================== FUNGSI CEK POSISI X & Y (VIEW ONLY) ====================
def menu_cek_posisi_xy():
  """Menu khusus untuk melihat koordinat X dan Y secara live tanpa eksekusi klik."""
  print("\n==================================================")
  print("       MODE CEK POSISI SUMBU X & Y (VIEW ONLY)    ")
  print("==================================================")
  print("Arahkan mouse Anda ke titik mana saja di layar.")
  if HAS_MSVCRT:
    print("  - Tekan [SPASI] untuk mencatat/menandai koordinat di layar.")
    print("  - Tekan [ENTER] atau [Q] untuk kembali ke Menu Utama.")
  else:
    print("  - Tekan [Ctrl + C] untuk kembali ke Menu Utama.")
  print("--------------------------------------------------\n")

  try:
    while True:
      x, y = pyautogui.position()
      print(f"Posisi Mouse Sekarang ->  X: {x:<5} | Y: {y:<5}   ", end="\r")

      if HAS_MSVCRT and msvcrt.kbhit():
        tombol = msvcrt.getch()
        # Jika menekan ENTER (b'\r') atau huruf q/Q, keluar ke Menu Utama
        if tombol in [b"\r", b"\n", b"q", b"Q", b"\x1b"]:
          print("\n\nKembali ke Menu Utama...")
          break
        # Jika menekan SPASI (b' '), cetak koordinat tersebut di baris baru agar mudah dicatat
        elif tombol == b" ":
          print(f"\n[DICATAT] Koordinat ditandai pada -> X={x}, Y={y}")

      time.sleep(0.05)
  except KeyboardInterrupt:
    print("\n\nKembali ke Menu Utama...")


# ==================== FUNGSI BANTU WAKTU ====================
def parse_delay(teks):
  """Mengubah input delay (contoh: '10d', '5m', '1j 30m', atau '00:05:00') menjadi total detik."""
  teks = teks.strip().lower().replace(",", ".")

  if ":" in teks or (teks.count(".") == 2):
    bagian = teks.replace(".", ":").split(":")
    if len(bagian) == 2:
      return int(bagian[0]) * 60 + int(bagian[1])
    elif len(bagian) == 3:
      return int(bagian[0]) * 3600 + int(bagian[1]) * 60 + int(bagian[2])

  total_detik = 0
  cocok = re.findall(r"(\d+)\s*([jmd]?)", teks)
  if not cocok:
    raise ValueError("Format tidak dikenali")

  for nilai_str, satuan in cocok:
    if not nilai_str:
      continue
    nilai = int(nilai_str)
    if satuan == "j":
      total_detik += nilai * 3600
    elif satuan == "m":
      total_detik += nilai * 60
    else:
      total_detik += nilai

  return total_detik


def format_sisa(total_detik):
  jam, sisa = divmod(max(0, int(total_detik)), 3600)
  menit, detik = divmod(sisa, 60)
  return f"{jam:02d}j {menit:02d}m {detik:02d}d"


def minta_waktu(pesan, waktu_acuan):
  """Meminta input jam dari user dan mengembalikan objek datetime beserta string jam."""
  while True:
    waktu_input = input(pesan).strip().replace(".", ":")
    bagian = waktu_input.split(":")
    try:
      if len(bagian) == 2:
        t_hour, t_minute, t_second = int(bagian[0]), int(bagian[1]), 5
      elif len(bagian) == 3:
        t_hour, t_minute, t_second = (
            int(bagian[0]),
            int(bagian[1]),
            int(bagian[2]),
        )
      else:
        raise ValueError

      if 0 <= t_hour <= 23 and 0 <= t_minute <= 59 and 0 <= t_second <= 59:
        break
      print("Gunakan rentang waktu 00:00 sampai 23:59.\n")
    except ValueError:
      print("Format salah! Contoh penulisan: 08.10 atau 08:10:05\n")

  target_dt = waktu_acuan.replace(
      hour=t_hour, minute=t_minute, second=t_second, microsecond=0
  )
  while target_dt <= waktu_acuan:
    target_dt += datetime.timedelta(days=1)

  return target_dt, target_dt.strftime("%H:%M:%S")


# ==================== FUNGSI PENGATURAN TITIK KLIK ====================
def atur_titik_klik(jumlah_klik, label_jadwal=""):
  """Mengatur koordinat (Auto / Manual / Ambil dari Config) dan delay."""
  daftar_klik = []
  prefix = f"[{label_jadwal}] " if label_jadwal else ""
  semua_config = muat_config()

  for idx in range(1, jumlah_klik + 1):
    print(f"\n  --- {prefix}PENGATURAN TITIK KLIK #{idx} ---")
    nama_titik = input(
        f"  Beri nama untuk Klik #{idx} (opsional, contoh: Continue / Not"
        " Now): "
    ).strip()
    if not nama_titik:
      nama_titik = f"Klik #{idx}"

    delay_detik = 0
    if idx > 1:
      print(
          f"  Masukkan delay sebelum mengeklik '{nama_titik}' ('d'=detik,"
          " 'm'=menit, 'j'=jam):"
      )
      while True:
        try:
          inp_delay = input(
              f"  Delay setelah Klik #{idx-1} -> Klik #{idx} (contoh: 10d, 5m,"
              " 1j): "
          ).strip()
          delay_detik = parse_delay(inp_delay)
          if delay_detik > 0:
            print(f"  Delay dikunci: {format_sisa(delay_detik)}")
            break
          print("  Delay harus lebih dari 0 detik!")
        except Exception:
          print("  Format salah! Contoh input: 10d atau 5m atau 1j 30m")

    print(f"\n  Pilih cara menentukan sumbu X dan Y untuk '{nama_titik}':")
    print("    1. Otomatis (Arahkan kursor mouse & tunggu 5 detik)")
    print("    2. Manual (Ketik angka sumbu X dan Y sendiri)")
    if semua_config:
      print("    3. Ambil dari Config Tersimpan")

    opsi_valid = ["1", "2", "3"] if semua_config else ["1", "2"]
    while True:
      metode_xy = input(
          f"  Pilih metode ({'/'.join(opsi_valid)}): "
      ).strip()
      if metode_xy in opsi_valid:
        break
      print("  Pilihan tidak valid!")

    if metode_xy == "1":
      input(
          f"  Tekan [ENTER] lalu arahkan mouse ke '{nama_titik}' dalam 5"
          " detik..."
      )
      for i in range(5, 0, -1):
        print(f"  Mengunci posisi '{nama_titik}' dalam {i} detik...", end="\r")
        time.sleep(1)
      x, y = pyautogui.position()
      print(f"\n  Koordinat '{nama_titik}' dikunci (Auto): X={x}, Y={y}")

    elif metode_xy == "2":
      while True:
        try:
          inp_xy = input(
              f"  Masukkan sumbu X dan Y untuk '{nama_titik}' (contoh: 1539,"
              " 256): "
          ).strip()
          angka = re.findall(r"-?\d+", inp_xy)
          if len(angka) >= 2:
            x, y = int(angka[0]), int(angka[1])
          elif len(angka) == 1:
            x = int(angka[0])
            y = int(input("  Masukkan sumbu Y: ").strip())
          else:
            raise ValueError
          print(f"  Koordinat '{nama_titik}' disimpan (Manual): X={x}, Y={y}")
          break
        except ValueError:
          print("  Input tidak valid! Masukkan angka seperti: 1539, 256")

    elif metode_xy == "3":
      nama_list = list(semua_config.keys())
      print("\n  Daftar Config Tersimpan:")
      for i_c, n_c in enumerate(nama_list, 1):
        k_pertama = semua_config[n_c][0]
        print(
            f"    {i_c}. {n_c} -> ({k_pertama['x']}, {k_pertama['y']})"
        )
      while True:
        try:
          pil_c = int(input("  Pilih nomor config: ").strip())
          if 1 <= pil_c <= len(nama_list):
            cfg_terpilih = semua_config[nama_list[pil_c - 1]][0]
            x, y = cfg_terpilih["x"], cfg_terpilih["y"]
            if nama_titik == f"Klik #{idx}":
              nama_titik = cfg_terpilih["nama"]
            print(
                f"  Koordinat diambil dari config '{nama_list[pil_c - 1]}':"
                f" X={x}, Y={y}"
            )
            break
          print("  Nomor tidak ada di daftar!")
        except ValueError:
          print("  Masukkan angka nomor config!")

    pyautogui.moveTo(x, y, duration=0.4)
    daftar_klik.append(
        {"nama": nama_titik, "x": x, "y": y, "delay": delay_detik}
    )

  return daftar_klik


# ==================== MENU KELOLA CONFIG ====================
def menu_kelola_config():
  """Menu untuk membuat, melihat, atau menghapus config."""
  while True:
    semua_config = muat_config()
    print("\n==================================================")
    print("               MENU KELOLA CONFIG                 ")
    print("==================================================")
    print("1. Buat / Simpan Config Baru (Contoh: Config Continue)")
    print("2. Lihat Daftar Config Tersimpan")
    print("3. Hapus Config")
    print("4. Kembali ke Menu Utama")

    pil = input("\nPilih menu (1 / 2 / 3 / 4): ").strip()

    if pil == "1":
      print("\n--- BUAT CONFIG BARU ---")
      nama_cfg = input(
          "Masukkan nama config (contoh: Contunies / paket_kerja): "
      ).strip()
      if not nama_cfg:
        print("Nama config tidak boleh kosong!")
        continue

      while True:
        try:
          jml = int(
              input(
                  f"Berapa titik klik yang ingin disimpan di config"
                  f" '{nama_cfg}'? (ketik 1 jika hanya Continue): "
              ).strip()
          )
          if jml >= 1:
            break
          print("Minimal 1 titik klik!")
        except ValueError:
          print("Masukkan angka yang valid!")

      klik_list = atur_titik_klik(jml, label_jadwal=f"Config: {nama_cfg}")
      semua_config[nama_cfg] = klik_list
      simpan_config(semua_config)
      print(
          f"\n[SUKSES] Config '{nama_cfg}' ({jml} klik) berhasil disimpan ke"
          f" {CONFIG_FILE}!"
      )

    elif pil == "2":
      print("\n--- DAFTAR CONFIG TERSIMPAN ---")
      if not semua_config:
        print("Belum ada config yang disimpan.")
      else:
        for i, (nama_c, k_list) in enumerate(semua_config.items(), 1):
          print(f"\n{i}. Nama Config: [{nama_c}] ({len(k_list)} Klik)")
          for idx_k, k in enumerate(k_list, 1):
            d_info = (
                "Langsung saat jadwal tiba"
                if idx_k == 1
                else f"Delay +{format_sisa(k['delay'])}"
            )
            print(
                f"   -> Klik #{idx_k} ({k['nama']}): X={k['x']}, Y={k['y']} |"
                f" {d_info}"
            )

    elif pil == "3":
      if not semua_config:
        print("\nBelum ada config untuk dihapus.")
        continue
      nama_list = list(semua_config.keys())
      print("\n--- HAPUS CONFIG ---")
      for i, n_c in enumerate(nama_list, 1):
        print(f"{i}. {n_c}")
      try:
        idx_hapus = int(
            input("Masukkan nomor config yang ingin dihapus (0 = batal): ")
            .strip()
        )
        if 1 <= idx_hapus <= len(nama_list):
          target_hapus = nama_list[idx_hapus - 1]
          del semua_config[target_hapus]
          simpan_config(semua_config)
          print(f"Config '{target_hapus}' berhasil dihapus!")
      except ValueError:
        print("Batal menghapus.")

    elif pil == "4":
      break
    else:
      print("Pilihan tidak valid!")


def pilih_config_tersimpan():
  """Memilih config dari daftar untuk dimasukkan ke dalam jadwal."""
  semua_config = muat_config()
  nama_list = list(semua_config.keys())

  print("\nDaftar Config Tersedia:")
  for i, n_c in enumerate(nama_list, 1):
    k_list = semua_config[n_c]
    ringkasan = ", ".join([f"{k['nama']}({k['x']},{k['y']})" for k in k_list])
    print(f"  {i}. [{n_c}] -> {len(k_list)} Klik: {ringkasan}")

  while True:
    try:
      pil = int(input("Pilih nomor config yang ingin digunakan: ").strip())
      if 1 <= pil <= len(nama_list):
        nama_terpilih = nama_list[pil - 1]
        klik_copy = [dict(k) for k in semua_config[nama_terpilih]]
        return nama_terpilih, klik_copy
      print("Nomor tidak ada di dalam daftar!")
    except ValueError:
      print("Masukkan angka nomor config!")


# ==================== PROGRAM UTAMA ====================
while True:
  print("\n==================================================")
  print("          AUTOCLICK-MAESTRO (COMPLETE)            ")
  print("        Licensed & Created by: BLUZ TEKNO         ")
  print("==================================================")
  print("Pilih Mode Eksekusi:")
  print("1. Mode 1 Kali Klik (Atur Langsung)")
  print("2. Mode Multi-Klik (1 Jadwal Waktu, Banyak Klik)")
  print("3. Mode Multi-Jadwal & Multi-Klik (Atur Langsung)")
  print("4. Jalankan dari Config Tersimpan (Bisa 1 Jadwal / Multi-Jadwal)")
  print("5. Menu Config (Buat Config Baru / Lihat / Hapus Config)")
  print("6. Cek Posisi Sumbu X dan Y (Hanya View / Tanpa Eksekusi)")

  mode_utama = input("\nMasukkan pilihan menu (1 / 2 / 3 / 4 / 5 / 6): ").strip()

  if mode_utama == "5":
    menu_kelola_config()
    continue
  elif mode_utama == "6":
    menu_cek_posisi_xy()
    continue
  elif mode_utama in ["1", "2", "3", "4"]:
    if mode_utama == "4" and not muat_config():
      print(
          "\n[!] Anda belum memiliki Config tersimpan! Silakan buat terlebih"
          " dahulu:"
      )
      menu_kelola_config()
      if not muat_config():
        continue
    break
  else:
    print("Pilihan tidak valid! Silakan ketik 1, 2, 3, 4, 5, atau 6.")

daftar_jadwal = []
waktu_acuan = datetime.datetime.now()

# --- OPSI 1: MODE 1 KALI KLIK ---
if mode_utama == "1":
  print("\n--- MODE 1 KALI KLIK ---")
  t_dt, t_str = minta_waktu(
      "Masukkan jam target klik (contoh 08.10 atau 08:10:05): ", waktu_acuan
  )
  klik_list = atur_titik_klik(1)
  daftar_jadwal.append(
      {"nomor": 1, "target_dt": t_dt, "target_str": t_str, "klik_list": klik_list}
  )

# --- OPSI 2: MODE MULTI-KLIK (1 WAKTU) ---
elif mode_utama == "2":
  print("\n--- MODE MULTI-KLIK (1 JADWAL WAKTU) ---")
  while True:
    try:
      jml = int(
          input(
              "Berapa titik lokasi yang ingin diklik berurutan? (contoh: 2): "
          ).strip()
      )
      if jml >= 2:
        break
      print("Untuk Multi-Klik, masukkan minimal 2 titik klik.")
    except ValueError:
      print("Masukkan angka yang valid!")

  t_dt, t_str = minta_waktu(
      "Masukkan jam target Klik #1 (contoh 08.10 atau 08:10:05): ", waktu_acuan
  )
  klik_list = atur_titik_klik(jml)
  daftar_jadwal.append(
      {"nomor": 1, "target_dt": t_dt, "target_str": t_str, "klik_list": klik_list}
  )

# --- OPSI 3: MODE MULTI-JADWAL & MULTI-KLIK (MANUAL/AUTO) ---
elif mode_utama == "3":
  nomor_jadwal = 1
  while True:
    print(f"\n##################################################")
    print(f"             PENGATURAN JADWAL #{nomor_jadwal}                 ")
    print(f"##################################################")

    t_dt, t_str = minta_waktu(
        f"Masukkan jam mulai untuk Jadwal #{nomor_jadwal} (contoh 08.10,"
        " 13.00, 17.30): ",
        waktu_acuan,
    )
    waktu_acuan = t_dt

    while True:
      try:
        jml = int(
            input(
                f"Berapa kali klik yang ingin dijalankan pada jam {t_str}?"
                " (contoh: 2): "
            ).strip()
        )
        if jml >= 1:
          break
        print("Masukkan minimal 1 kali klik.")
      except ValueError:
        print("Masukkan angka yang valid!")

    klik_list = atur_titik_klik(
        jml, label_jadwal=f"Jadwal #{nomor_jadwal} - {t_str}"
    )
    daftar_jadwal.append({
        "nomor": nomor_jadwal,
        "target_dt": t_dt,
        "target_str": t_str,
        "klik_list": klik_list,
    })

    print("\n--------------------------------------------------")
    print("Pilih langkah selanjutnya:")
    print("  1. Tambah Jadwal Jam Berikutnya")
    print("  2. Selesaikan Pengaturan & Jalankan Bot Sekarang")

    while True:
      langkah = input("Masukkan pilihan (1 = Tambah, 2 = Selesaikan): ").strip()
      if langkah in ["1", "2"]:
        break
    if langkah == "2":
      break
    nomor_jadwal += 1

# --- OPSI 4: JALANKAN DARI CONFIG TERSIMPAN (1 JADWAL / MULTI-JADWAL) ---
elif mode_utama == "4":
  nomor_jadwal = 1
  while True:
    print(f"\n##################################################")
    print(f"        PENGATURAN JADWAL CONFIG #{nomor_jadwal}              ")
    print(f"##################################################")

    nama_cfg, klik_list = pilih_config_tersimpan()
    print(f"--> Config [{nama_cfg}] dipilih ({len(klik_list)} titik klik).")

    t_dt, t_str = minta_waktu(
        f"Masukkan jam eksekusi untuk Config [{nama_cfg}] pada Jadwal"
        f" #{nomor_jadwal} (contoh 08.10 / 13.00): ",
        waktu_acuan,
    )
    waktu_acuan = t_dt

    daftar_jadwal.append({
        "nomor": nomor_jadwal,
        "target_dt": t_dt,
        "target_str": t_str,
        "klik_list": klik_list,
        "nama_config": nama_cfg,
    })

    print("\n--------------------------------------------------")
    print(
        f"Jadwal #{nomor_jadwal} menggunakan Config [{nama_cfg}] pada pukul"
        f" {t_str} berhasil disiapkan!"
    )
    print("Pilih langkah selanjutnya:")
    print("  1. Tambah Jadwal Jam Berikutnya (Multi-Jadwal)")
    print("  2. Selesaikan & Jalankan Bot Sekarang")

    while True:
      langkah = input("Masukkan pilihan (1 = Tambah Jadwal, 2 = Jalankan): ").strip()
      if langkah in ["1", "2"]:
        break
    if langkah == "2":
      break
    nomor_jadwal += 1

# ==================== RINGKASAN & EKSEKUSI ====================
print("\n==================================================")
print("         RINGKASAN SELURUH JADWAL & KLIK          ")
print("==================================================")
for j in daftar_jadwal:
  info_cfg = f" (Config: {j['nama_config']})" if "nama_config" in j else ""
  print(
      f"\n[SESI JADWAL #{j['nomor']}{info_cfg}] Waktu Mulai: Pukul"
      f" {j['target_str']} | Total: {len(j['klik_list'])} Klik"
  )
  for idx, k in enumerate(j["klik_list"], 1):
    info = (
        f"Pada pukul {j['target_str']}"
        if idx == 1
        else f"Delay +{format_sisa(k['delay'])} setelah Klik #{idx-1}"
    )
    print(
        f"   -> Klik #{idx} ({k['nama']}): Koordinat ({k['x']}, {k['y']}) |"
        f" {info}"
    )
print("\nJangan geser atau scroll jendela aplikasi target.")
print("==================================================\n")

# Menjalankan setiap sesi jadwal secara berurutan
for j in daftar_jadwal:
  no_j = j["nomor"]
  t_dt = j["target_dt"]
  t_str = j["target_str"]
  klik_list = j["klik_list"]
  klik_pertama = klik_list[0]

  print(
      f">>> Menunggu Sesi Jadwal #{no_j} (Pukul {t_str}) - Total"
      f" {len(klik_list)} Klik <<<"
  )

  while True:
    now = datetime.datetime.now()
    cur_x, cur_y = pyautogui.position()
    selisih = int((t_dt - now).total_seconds())

    if selisih <= 0:
      print(
          f"\n[{now.strftime('%H:%M:%S')}] Jadwal #{no_j} tiba! Mengeklik"
          f" Klik #1 '{klik_pertama['nama']}' di ({klik_pertama['x']},"
          f" {klik_pertama['y']})..."
      )
      pyautogui.click(klik_pertama["x"], klik_pertama["y"])
      print(
          f"Jadwal #{no_j} - Klik #1 ({klik_pertama['nama']}) berhasil"
          " dieksekusi!"
      )
      break

    print(
        f"[{now.strftime('%H:%M:%S')}] Jdwl#{no_j}({t_str}) | Sisa:"
        f" {format_sisa(selisih)} | Tgt:({klik_pertama['x']},{klik_pertama['y']})"
        f" | Pos:({cur_x},{cur_y})   ",
        end="\r",
    )
    time.sleep(1)

  for idx in range(1, len(klik_list)):
    item = klik_list[idx]
    sisa_delay = item["delay"]
    print(
        f"\nMenunggu delay untuk Jadwal #{no_j} - Klik #{idx+1}"
        f" ({item['nama']})..."
    )

    while sisa_delay > 0:
      now = datetime.datetime.now()
      cur_x, cur_y = pyautogui.position()
      print(
          f"[{now.strftime('%H:%M:%S')}] Jdwl#{no_j}->Klik#{idx+1} | Sisa:"
          f" {format_sisa(sisa_delay)} | Tgt:({item['x']},{item['y']}) |"
          f" Pos:({cur_x},{cur_y})   ",
          end="\r",
      )
      time.sleep(1)
      sisa_delay -= 1

    now = datetime.datetime.now()
    print(
        f"\n[{now.strftime('%H:%M:%S')}] Delay selesai! Mengeklik Jadwal"
        f" #{no_j} - Klik #{idx+1} '{item['nama']}' di ({item['x']},"
        f" {item['y']})..."
    )
    pyautogui.click(item["x"], item["y"])
    print(f"Jadwal #{no_j} - Klik #{idx+1} ({item['nama']}) berhasil dieksekusi!")

  print(f"\n--- SESI JADWAL #{no_j} SELESAI ---\n")

print("=== SELURUH RANGKAIAN JADWAL AUTO KLIK SELESAI ===")
