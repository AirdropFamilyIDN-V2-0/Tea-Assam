from web3 import Web3
import time
from eth_account import Account

print("[+]===============================[+]")
print("[+]       AUTO TX TEA ASEM        [+]")
print("[+]     KE LIST ADDRESS.TXT       [+]")
print("[+]      Airdrop Family IDN       [+]")
print("[+] https://t.me/AirdropFamilyIDN [+]")
print("[+]===============================[+]")

rpc_url = "https://assam-rpc.tea.xyz"
chain_id = 93384
web3 = Web3(Web3.HTTPProvider(rpc_url))

if web3.is_connected():
    print("[+] Web3 berhasil tersambung ke jaringan TEA...")
else:
    print("[+] Gagal menyambung ke jaringan TEA. Periksa RPC atau koneksi Anda!")
    exit()

def transfer_tea(sender, sender_key, recipient, amount):
    try:
        tx_config = {
            'chainId': chain_id,
            'from': sender,
            'to': recipient,
            'value': web3.to_wei(amount, 'ether'),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender)
        }
        estimated_gas = web3.eth.estimate_gas(tx_config)
        tx_config['gas'] = estimated_gas

        sender_balance = web3.eth.get_balance(sender)
        total_cost = web3.to_wei(amount, 'ether') + (estimated_gas * web3.eth.gas_price)

        if sender_balance < total_cost:
            print(f"[+] Saldo tidak cukup! Dibutuhkan {web3.from_wei(total_cost, 'ether')} $TEA, "
                  f"tetapi hanya tersedia {web3.from_wei(sender_balance, 'ether')} $TEA.")
            return False

        signed_tx = web3.eth.account.sign_transaction(tx_config, sender_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_id = web3.to_hex(tx_hash)

        print(f"[+] Berhasil mengirim $TEA ke {recipient}. TX ID: {tx_id}")
        return True

    except Exception as e:
        print(f"[+] Error saat mengirim transaksi ke {recipient}: {str(e)}")
        return False

file_name = "listaddress.txt"
try:
    with open(file_name, "r") as file:
        address_list = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
    print(f"[+] File {file_name} tidak ditemukan. Pastikan file ini ada di direktori yang sama dengan script!")
    exit()

sender_key = input("[+] Masukkan Private Key Wallet Anda: ")
sender_account = Account.from_key(sender_key)
amount = float(input("[+] Masukkan jumlah $TEA yang akan dikirim: "))
sleep_time = int(input("[+] Masukkan waktu jeda antar transaksi (dalam detik): "))

for i, recipient in enumerate(address_list, start=1):
    print(f"[+] Mengirim transaksi ke alamat #{i}: {recipient}...")
    success = transfer_tea(web3.to_checksum_address(sender_account.address), sender_key, web3.to_checksum_address(recipient), amount)
    if success:
        print(f"[+] Menunggu selama {sleep_time} detik sebelum melanjutkan transaksi berikutnya...")
        time.sleep(sleep_time)
    else:
        print("[+] Gagal mengirim transaksi. Melanjutkan ke alamat berikutnya.")

print("[+] Semua transaksi selesai.")

