#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        XENEA UBUSUNA — AUTO TX BOT v1.2                     ║
║        Network: Xenea Ubusuna | Chain ID: 1096              ║
║        by DropsterMind                                       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import getpass
from datetime import datetime, timedelta
from pathlib import Path

try:
    from web3 import Web3
    from eth_account import Account
    from dotenv import load_dotenv
except ImportError:
    print("\n[!] Dependency belum terinstall. Jalankan perintah berikut:")
    print("    pip install web3 eth-account python-dotenv\n")
    sys.exit(1)

# ─────────────────────────────────────────────
#  NETWORK CONFIG — Xenea Ubusuna
# ─────────────────────────────────────────────
NETWORK = {
    "name":     "Xenea Ubusuna",
    "rpc":      "https://rpc-ubusuna.xeneascan.com",
    "chain_id": 1096,
    "symbol":   "TXENE",
    "explorer": "https://ubusuna.xeneascan.com/tx/",
}

ENV_FILE       = ".env"
CYCLE_HOURS    = 24          # reset cycle dalam jam
CYCLE_SECONDS  = CYCLE_HOURS * 3600

# ─────────────────────────────────────────────
#  ANSI COLOR HELPERS
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"

def clr(text, *colors):
    return "".join(colors) + str(text) + C.RESET

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(clr("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██╗  ██╗███████╗███╗   ██╗███████╗ █████╗                     ║
║   ╚██╗██╔╝██╔════╝████╗  ██║██╔════╝██╔══██╗                    ║
║    ╚███╔╝ █████╗  ██╔██╗ ██║█████╗  ███████║                    ║
║    ██╔██╗ ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██║                    ║
║   ██╔╝ ██╗███████╗██║ ╚████║███████╗██║  ██║                    ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  AUTO TX BOT     ║
║                                                                  ║
║   Network  : Xenea Ubusuna          Chain ID : 1096             ║
║   Symbol   : TXENE                  Version  : 1.2.0            ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║              by  D R O P S T E R M I N D  ★                    ║
╚══════════════════════════════════════════════════════════════════╝
""", C.CYAN, C.BOLD))

def watermark():
    print(clr("  ★ by DropsterMind", C.MAGENTA, C.BOLD) +
          clr("  |  Xenea Ubusuna AutoTX Bot v1.2", C.DIM))
    print()

def log(level, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {
        "info":  clr("  INFO ", C.BLUE,    C.BOLD),
        "ok":    clr("    OK ", C.GREEN,   C.BOLD),
        "warn":  clr("  WARN ", C.YELLOW,  C.BOLD),
        "error": clr(" ERROR ", C.RED,     C.BOLD),
        "tx":    clr("    TX ", C.CYAN,    C.BOLD),
        "step":  clr("  STEP ", C.MAGENTA, C.BOLD),
        "env":   clr("   ENV ", C.MAGENTA, C.BOLD),
        "timer": clr(" TIMER ", C.YELLOW,  C.BOLD),
        "cycle": clr(" CYCLE ", C.GREEN,   C.BOLD),
    }.get(level, "  LOG  ")
    print(f"  {clr(ts, C.DIM)}  {prefix}  {msg}")

def separator(char="─", width=68, color=C.DIM):
    print(clr(char * width, color))

def section(title):
    separator()
    print(clr(f"  ◆ {title}", C.YELLOW, C.BOLD))
    separator()

# ─────────────────────────────────────────────
#  WEB3 CONNECTION
# ─────────────────────────────────────────────
def connect_rpc():
    log("step", "Menghubungkan ke " + clr(NETWORK["name"], C.CYAN, C.BOLD) + " ...")
    w3 = Web3(Web3.HTTPProvider(NETWORK["rpc"]))
    if not w3.is_connected():
        log("error", "Gagal terhubung ke RPC. Periksa koneksi internet Anda.")
        sys.exit(1)
    block = w3.eth.block_number
    log("ok", "Terhubung!  Block terbaru: " + clr(block, C.GREEN, C.BOLD))
    return w3

# ─────────────────────────────────────────────
#  .ENV MANAGER
# ─────────────────────────────────────────────
def ensure_env_file():
    if not Path(ENV_FILE).exists():
        with open(ENV_FILE, "w") as f:
            f.write("# Xenea Ubusuna AutoTX Bot — Konfigurasi\n")
            f.write("# JANGAN bagikan file ini kepada siapa pun!\n\n")
            f.write("PRIVATE_KEY=\n")
        log("env", "File " + clr(ENV_FILE, C.CYAN) + " baru dibuat.")
    gitignore = Path(".gitignore")
    if gitignore.exists():
        if ".env" not in gitignore.read_text():
            with open(gitignore, "a") as f:
                f.write(".env\n")
    else:
        with open(gitignore, "w") as f:
            f.write(".env\n")

def save_pk_to_env(pk):
    ensure_env_file()
    lines = Path(ENV_FILE).read_text().splitlines(keepends=True)
    new_lines = []
    found = False
    for line in lines:
        if line.strip().startswith("PRIVATE_KEY="):
            new_lines.append("PRIVATE_KEY=" + pk + "\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append("PRIVATE_KEY=" + pk + "\n")
    Path(ENV_FILE).write_text("".join(new_lines))

def load_pk_from_env():
    load_dotenv(ENV_FILE, override=True)
    pk = os.getenv("PRIVATE_KEY", "").strip()
    return pk if pk else None

# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
def login(w3):
    section("LOGIN WALLET")
    ensure_env_file()
    pk = load_pk_from_env()

    if pk:
        log("env", "Private key ditemukan di " + clr(ENV_FILE, C.CYAN))
        if not pk.startswith("0x"):
            pk = "0x" + pk
        try:
            account     = Account.from_key(pk)
            balance_wei = w3.eth.get_balance(account.address)
            balance     = float(w3.from_wei(balance_wei, "ether"))
            sym         = NETWORK["symbol"]
            log("ok",   "Wallet berhasil dimuat dari .env!")
            log("info", "Address  : " + clr(account.address, C.CYAN))
            log("info", "Balance  : " + clr(str(round(balance, 6)) + " " + sym, C.GREEN, C.BOLD))
            print()
            return account, pk, balance
        except Exception as e:
            log("error", "Private key di .env tidak valid: " + str(e))
            log("warn",  "Meminta private key ulang ...")
            print()

    log("info", "Masukkan private key wallet Anda.")
    log("warn", "Key dapat disimpan ke " + clr(ENV_FILE, C.CYAN) + " agar tidak perlu input ulang.")
    print()

    while True:
        pk_raw = getpass.getpass("  Private Key: ").strip()
        if not pk_raw:
            log("warn", "Input kosong, coba lagi.")
            continue
        pk = pk_raw if pk_raw.startswith("0x") else "0x" + pk_raw
        try:
            account     = Account.from_key(pk)
            balance_wei = w3.eth.get_balance(account.address)
            balance     = float(w3.from_wei(balance_wei, "ether"))
            print()
            log("ok", "Private key valid!")
            save = input(clr("  Simpan ke " + ENV_FILE + " untuk sesi berikutnya? (y/n): ", C.YELLOW)).strip().lower()
            if save == "y":
                save_pk_to_env(pk)
                log("env", "Private key disimpan ke " + clr(ENV_FILE, C.GREEN))
            else:
                log("warn", "Private key TIDAK disimpan.")
            print()
            sym = NETWORK["symbol"]
            log("ok",   "Wallet berhasil dimuat!")
            log("info", "Address  : " + clr(account.address, C.CYAN))
            log("info", "Balance  : " + clr(str(round(balance, 6)) + " " + sym, C.GREEN, C.BOLD))
            print()
            return account, pk, balance
        except Exception as e:
            log("error", "Private key tidak valid: " + str(e))
            print()

# ─────────────────────────────────────────────
#  LOAD WALLET LIST
# ─────────────────────────────────────────────
def load_wallets(filepath="wallet.txt"):
    path = Path(filepath)
    if not path.exists():
        log("warn", "File '" + filepath + "' tidak ditemukan. Membuat file contoh ...")
        with open(filepath, "w") as f:
            f.write("# Masukkan alamat wallet tujuan (satu per baris)\n")
            f.write("# Contoh:\n")
            f.write("# 0xAbCdEf1234567890AbCdEf1234567890AbCdEf12\n")
        log("info", "File '" + filepath + "' telah dibuat. Isi dengan alamat tujuan, lalu jalankan ulang.")
        sys.exit(0)

    wallets = []
    with open(filepath) as f:
        for line in f:
            addr = line.strip()
            if addr and not addr.startswith("#"):
                if Web3.is_address(addr):
                    wallets.append(Web3.to_checksum_address(addr))
                else:
                    log("warn", "Alamat tidak valid, dilewati: " + addr)

    if not wallets:
        log("error", "Tidak ada alamat valid di wallet.txt")
        sys.exit(1)

    log("ok", "Dimuat " + clr(len(wallets), C.GREEN, C.BOLD) + " alamat tujuan.")
    print()
    return wallets

# ─────────────────────────────────────────────
#  SEND CONFIG INPUT
# ─────────────────────────────────────────────
def get_send_config(balance):
    section("KONFIGURASI PENGIRIMAN")
    sym = NETWORK["symbol"]

    while True:
        try:
            raw = input(clr("  Jumlah " + sym + " per TX (contoh: 0.001): ", C.WHITE)).strip()
            amount = float(raw)
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            log("warn", "Masukkan angka positif yang valid.")

    while True:
        try:
            raw = input(clr("  Jumlah TX per siklus (0 = kirim ke semua wallet): ", C.WHITE)).strip()
            tx_count = int(raw)
            if tx_count < 0:
                raise ValueError
            break
        except ValueError:
            log("warn", "Masukkan bilangan bulat >= 0.")

    while True:
        try:
            raw = input(clr("  Delay MIN antar TX dalam detik (contoh: 15): ", C.WHITE)).strip()
            delay_min = float(raw)
            if delay_min < 0:
                raise ValueError
            break
        except ValueError:
            log("warn", "Masukkan angka >= 0.")

    while True:
        try:
            raw = input(clr("  Delay MAX antar TX dalam detik (contoh: 20): ", C.WHITE)).strip()
            delay_max = float(raw)
            if delay_max < delay_min:
                log("warn", "Delay MAX harus >= Delay MIN (" + str(delay_min) + ").")
                continue
            break
        except ValueError:
            log("warn", "Masukkan angka >= 0.")

    print()
    tx_label    = "SEMUA WALLET" if tx_count == 0 else str(tx_count)
    delay_label = str(delay_min) + "s – " + str(delay_max) + "s  (random)"
    log("info", "Amount per TX  : " + clr(str(amount) + " " + sym, C.CYAN, C.BOLD))
    log("info", "TX per siklus  : " + clr(tx_label, C.CYAN, C.BOLD))
    log("info", "Delay antar TX : " + clr(delay_label, C.CYAN, C.BOLD))
    log("info", "Reset siklus   : " + clr("Setiap " + str(CYCLE_HOURS) + " jam", C.CYAN, C.BOLD))
    log("info", "Urutan tujuan  : " + clr("RANDOM dari wallet.txt", C.CYAN, C.BOLD))
    log("info", "Saldo saat ini : " + clr(str(round(balance, 6)) + " " + sym, C.GREEN, C.BOLD))
    print()

    confirm = input(clr("  Mulai kirim? (y/n): ", C.YELLOW)).strip().lower()
    if confirm != "y":
        log("warn", "Dibatalkan oleh pengguna.")
        sys.exit(0)
    print()

    return amount, tx_count, delay_min, delay_max

# ─────────────────────────────────────────────
#  SEND TRANSACTION
# ─────────────────────────────────────────────
def send_tx(w3, account, pk, to_address, amount_eth):
    value_wei = w3.to_wei(amount_eth, "ether")
    nonce     = w3.eth.get_transaction_count(account.address, "pending")
    gas_price = w3.eth.gas_price

    tx = {
        "nonce":    nonce,
        "to":       to_address,
        "value":    value_wei,
        "gas":      21000,
        "gasPrice": gas_price,
        "chainId":  NETWORK["chain_id"],
    }

    signed  = w3.eth.account.sign_transaction(tx, pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()

# ─────────────────────────────────────────────
#  COUNTDOWN TIMER (24 jam)
# ─────────────────────────────────────────────
def countdown_24h(next_run_time):
    """Tampilkan countdown sampai next_run_time, update setiap detik."""
    separator("═", 68, C.YELLOW)
    print(clr("  ◆ MENUNGGU SIKLUS BERIKUTNYA (24 JAM)", C.YELLOW, C.BOLD))
    separator("═", 68, C.YELLOW)
    log("timer", "Siklus berikutnya : " + clr(next_run_time.strftime("%Y-%m-%d %H:%M:%S"), C.CYAN, C.BOLD))
    print()

    try:
        while True:
            remaining = next_run_time - datetime.now()
            if remaining.total_seconds() <= 0:
                break
            total_sec = int(remaining.total_seconds())
            hh = total_sec // 3600
            mm = (total_sec % 3600) // 60
            ss = total_sec % 60
            countdown_str = clr(f"  {hh:02d}:{mm:02d}:{ss:02d}", C.CYAN, C.BOLD)
            print(f"\r  {clr('⏳', C.YELLOW)} Sisa waktu  {countdown_str}  {clr('| Ctrl+C untuk berhenti', C.DIM)}   ", end="", flush=True)
            time.sleep(1)
        print()
    except KeyboardInterrupt:
        print()
        log("warn", "Bot dihentikan oleh pengguna saat menunggu.")
        sys.exit(0)

# ─────────────────────────────────────────────
#  SATU SIKLUS TX
# ─────────────────────────────────────────────
def run_cycle(w3, account, pk, wallets, amount, tx_count, delay_min, delay_max, cycle_num):
    sym = NETWORK["symbol"]
    section("SIKLUS #" + str(cycle_num) + " — AUTO TX MULAI")
    log("cycle", "Waktu mulai : " + clr(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), C.GREEN))

    # Tentukan daftar target: tx_count=0 → semua wallet, acak urutan
    pool = wallets.copy()
    random.shuffle(pool)
    targets = pool if tx_count == 0 else [pool[i % len(pool)] for i in range(tx_count)]

    success = 0
    failed  = 0
    total   = len(targets)

    try:
        for idx, to_addr in enumerate(targets, 1):
            bal_wei = w3.eth.get_balance(account.address)
            bal_eth = float(w3.from_wei(bal_wei, "ether"))

            label_idx = "TX " + clr(str(idx).zfill(3) + "/" + str(total).zfill(3), C.CYAN)
            label_to  = clr(to_addr[:10] + "..." + to_addr[-6:], C.WHITE)

            if bal_eth < amount:
                log("error", label_idx + "  Saldo tidak cukup! (" + str(round(bal_eth, 6)) + " < " + str(amount) + ")")
                break

            log("tx", label_idx + "  ➜  " + label_to + "  " + clr(str(amount) + " " + sym, C.GREEN))

            try:
                tx_hash = send_tx(w3, account, pk, to_addr, amount)
                success += 1
                log("ok", "Hash    : " + clr(tx_hash[:20] + "...", C.CYAN))
                log("ok", "Explorer: " + clr(NETWORK["explorer"] + tx_hash, C.BLUE))
            except Exception as e:
                failed += 1
                log("error", "Gagal: " + str(e)[:80])

            # Progress bar
            pct   = int((idx / total) * 30)
            bar   = clr("█" * pct, C.CYAN) + clr("░" * (30 - pct), C.DIM)
            saldo = clr(str(round(bal_eth - amount, 6)), C.GREEN)
            print("\n    [" + bar + "]  " + clr(str(idx), C.BOLD) + "/" + str(total) +
                  "  saldo≈" + saldo + " " + sym + "\n")

            if idx < total:
                wait = round(random.uniform(delay_min, delay_max), 2)
                log("info", "Menunggu " + clr(str(wait) + " detik", C.YELLOW, C.BOLD) +
                    clr("  (range: " + str(delay_min) + "s – " + str(delay_max) + "s)", C.DIM))
                time.sleep(wait)

    except KeyboardInterrupt:
        print()
        log("warn", "Dihentikan oleh pengguna (Ctrl+C)")
        raise

    # Ringkasan siklus
    separator("═", 68, C.CYAN)
    print(clr("  ◆ RINGKASAN SIKLUS #" + str(cycle_num), C.CYAN, C.BOLD))
    separator("═", 68, C.CYAN)
    log("info",  "TX Dikirim   : " + clr(success + failed, C.WHITE, C.BOLD))
    log("ok",    "Berhasil     : " + clr(success, C.GREEN, C.BOLD))
    if failed:
        log("error", "Gagal        : " + clr(failed, C.RED, C.BOLD))
    bal_final = float(w3.from_wei(w3.eth.get_balance(account.address), "ether"))
    log("info",  "Saldo akhir  : " + clr(str(round(bal_final, 6)) + " " + sym, C.CYAN, C.BOLD))
    log("cycle", "Siklus selesai: " + clr(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), C.GREEN))
    separator("═", 68, C.CYAN)
    print()
    watermark()

# ─────────────────────────────────────────────
#  MAIN — loop 24 jam
# ─────────────────────────────────────────────
def main():
    banner()
    watermark()

    w3                      = connect_rpc()
    account, pk, balance    = login(w3)
    wallets                 = load_wallets("wallet.txt")
    amount, tx_count, delay_min, delay_max = get_send_config(balance)

    cycle_num = 1

    while True:
        try:
            run_cycle(w3, account, pk, wallets, amount, tx_count, delay_min, delay_max, cycle_num)
        except KeyboardInterrupt:
            log("warn", "Bot dihentikan total.")
            sys.exit(0)

        cycle_num += 1
        next_run = datetime.now() + timedelta(seconds=CYCLE_SECONDS)
        countdown_24h(next_run)

        # Refresh saldo setelah countdown
        try:
            bal_wei = w3.eth.get_balance(account.address)
            balance = float(w3.from_wei(bal_wei, "ether"))
            sym     = NETWORK["symbol"]
            section("MEMULAI SIKLUS #" + str(cycle_num))
            log("cycle", "Saldo terkini : " + clr(str(round(balance, 6)) + " " + sym, C.GREEN, C.BOLD))
            print()
        except Exception as e:
            log("warn", "Gagal refresh saldo: " + str(e))

if __name__ == "__main__":
    main()
