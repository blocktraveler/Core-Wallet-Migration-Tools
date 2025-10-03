################################################################################################################

# Copyright (C) 2025 by Uwe Martens * www.namecoin.pro  * https://dotbit.app

################################################################################################################

import subprocess
import json
import os
import sys
import time

CLI_COMMAND = "namecoin-cli" # Change to "bitcoin-cli" if using Bitcoin Core

def main():
	# Export private keys for UTXOs
	try:
		unspent_output = subprocess.check_output([CLI_COMMAND, "listunspent"]).decode("utf-8")
		unspent = json.loads(unspent_output)
	except subprocess.CalledProcessError as e:
		print(f"Error running {CLI_COMMAND} listunspent: {e}")
		sys.exit(1)
	except json.JSONDecodeError:
		print("Error parsing JSON from listunspent.")
		sys.exit(1)

	utxo_count = 0
	with open("privkeys.txt", "w") as f:
		for item in unspent:
			address = item.get("address")
			if address:
				try:
					privkey_output = subprocess.check_output([CLI_COMMAND, "dumpprivkey", address]).decode("utf-8").strip()
					print(privkey_output)
					f.write(privkey_output + "\n")
					utxo_count += 1
				except subprocess.CalledProcessError as e:
					print(f"Error dumping privkey for {address}: {e}")

	print(f"\nNumber of UTXOs: {utxo_count}\n")

	# Export private keys for names (only if using Namecoin Core)
	if CLI_COMMAND == "namecoin-cli":
		time.sleep(5)
		try:
			name_list_output = subprocess.check_output([CLI_COMMAND, "name_list"]).decode("utf-8")
			name_list = json.loads(name_list_output)
		except subprocess.CalledProcessError as e:
			print(f"Error running {CLI_COMMAND} name_list: {e}")
			sys.exit(1)
		except json.JSONDecodeError:
			print("Error parsing JSON from name_list.")
			sys.exit(1)

		name_count = 0
		with open("privkeys.txt", "a") as f:
			for item in name_list:
				address = item.get("address")
				ismine = item.get("ismine")
				expires_in = item.get("expires_in", 0)

				if ismine is True and expires_in >= 1 and address:
					try:
						privkey_output = subprocess.check_output([CLI_COMMAND, "dumpprivkey", address]).decode("utf-8").strip()
						print(privkey_output)
						f.write(privkey_output + "\n")
						name_count += 1
					except subprocess.CalledProcessError as e:
						print(f"Error dumping privkey for {address}: {e}")

		print(f"\nNumber of names: {name_count}\n")
	else:
		print("\nSkipping name_list export as it's Namecoin-specific.\n")

	print("[INFO] Private keys exported to privkeys.txt.\n\n")
	input("Press Enter to exit...")

if __name__ == "__main__":
	main()