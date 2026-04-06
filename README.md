# 🤖 Xenea Ubusuna — AutoTX Bot

<div align="center">

![Version](https://img.shields.io/badge/version-1.2.0-cyan?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![Network](https://img.shields.io/badge/network-Xenea%20Ubusuna-purple?style=for-the-badge)
![Chain](https://img.shields.io/badge/chain_id-1096-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**Bot otomatis untuk mengirim transaksi native TXENE di jaringan Xenea Ubusuna.**  
Mendukung siklus 24 jam, pengiriman ke random address, dan delay acak antar TX.

*by DropsterMind ★*

</div>

---

## ✨ Fitur

- 🔐 **Login via Private Key** — input tersembunyi, disimpan aman di `.env`
- 🔄 **Siklus 24 Jam Otomatis** — bot reset dan ulangi pengiriman setiap 24 jam dengan countdown timer live
- 🎲 **Random Address** — urutan wallet tujuan diacak setiap siklus
- ⏱️ **Delay Random** — tentukan rentang delay min–max (contoh: 15s–20s), bot pilih acak tiap TX
- 📋 **Wallet List** — kelola daftar tujuan lewat file `wallet.txt`
- 📊 **Progress Bar & Ringkasan** — tampilan real-time per TX dan summary per siklus
- 🔗 **Explorer Link** — setiap TX sukses langsung menampilkan link ke block explorer
- 🛡️ **Auto `.gitignore`** — file `.env` otomatis diamankan dari Git

---

## 🌐 Detail Jaringan

| Parameter | Value |
|-----------|-------|
| Network Name | Xenea Ubusuna |
| RPC URL | `https://rpc-ubusuna.xeneascan.com` |
| Chain ID | `1096` |
| Currency Symbol | `TXENE` |
| Block Explorer | `https://ubusuna.xeneascan.com/` |

---

## ⚙️ Instalasi

### 1. Clone repository

```bash
git clone https://github.com/DropsterMind/XENEA-TESNET-BOT.git
cd XENEA-TESNET-BOT
```

### 2. Install dependencies

```bash
pip install web3 eth-account python-dotenv
or
pip3 install web3 eth-account python-dotenv
```

### 3. Siapkan daftar wallet tujuan

Buat file `wallet.txt` dan isi dengan alamat-alamat tujuan, satu per baris:

```
0xAbCdEf1234567890AbCdEf1234567890AbCdEf12
0x1234567890AbCdEf1234567890AbCdEf12345678
0xDeFaBc9876543210DeFaBc9876543210DeFaBc98
```

> Baris yang diawali `#` akan diabaikan (komentar).

### 4. (Opsional) Siapkan file `.env`

Salin contoh konfigurasi:

```bash
cp .env.example .env
```

Lalu isi private key di `.env`:

```env
PRIVATE_KEY=0xYourPrivateKeyHere
```

> Jika `.env` tidak disiapkan, bot akan meminta input saat pertama dijalankan dan menawarkan untuk menyimpannya.

---

## 🚀 Menjalankan Bot

```bash
python bot.py or python3 bot.py
```

---

## 🖥️ Alur Penggunaan

```
1. Bot terhubung ke RPC Xenea Ubusuna
2. Login wallet (dari .env atau input manual)
3. Konfigurasi:
   ├─ Jumlah TXENE per TX
   ├─ Jumlah TX per siklus  (0 = semua wallet)
   ├─ Delay MIN antar TX
   └─ Delay MAX antar TX
4. Konfirmasi → mulai siklus pertama
5. Bot kirim ke wallet secara random
6. Selesai → countdown 24 jam
7. Ulangi dari langkah 5 (loop selamanya)
```

---

## 📁 Struktur File

```
xenea-autotx-bot/
├── xenea_autotx.py     ← Script utama bot
├── wallet.txt          ← Daftar alamat wallet tujuan
├── .env                ← Private key (JANGAN di-commit!)
├── .env.example        ← Template konfigurasi
├── .gitignore          ← Dibuat otomatis oleh bot
└── README.md           ← Dokumentasi ini
```

---

## 🔧 Konfigurasi Lengkap

| Parameter | Deskripsi |
|-----------|-----------|
| `PRIVATE_KEY` di `.env` | Private key wallet pengirim |
| Jumlah TXENE per TX | Nominal yang dikirim per transaksi |
| Jumlah TX per siklus | Berapa TX dalam satu putaran (`0` = semua wallet) |
| Delay MIN | Batas bawah jeda antar TX (detik) |
| Delay MAX | Batas atas jeda antar TX (detik) |
| `CYCLE_HOURS` di script | Interval reset siklus (default: `24` jam) |

---

## ⚠️ Catatan Penting

> **JANGAN pernah membagikan file `.env` atau private key Anda kepada siapa pun.**

- Private key hanya disimpan di file `.env` lokal, tidak pernah dikirim ke mana pun
- File `.env` otomatis masuk `.gitignore` agar tidak ter-upload ke GitHub
- Pastikan saldo TXENE mencukupi sebelum menjalankan bot (termasuk estimasi gas)
- Bot akan berhenti otomatis jika saldo tidak mencukupi untuk TX berikutnya
- Tekan `Ctrl+C` kapan saja untuk menghentikan bot

---

## 📜 License

MIT License — bebas digunakan dan dimodifikasi.

---

<div align="center">

Made with ❤️ by **DropsterMind**

</div>
