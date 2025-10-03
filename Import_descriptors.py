################################################################################################################

# Copyright (C) 2025 by Uwe Martens * www.namecoin.pro  * https://dotbit.app

################################################################################################################

import subprocess
import json
import os
import sys
import time

CLI_COMMAND = "namecoin-cli" # Change to "bitcoin-cli" if using Bitcoin Core
PRIVKEYS_FILE = "privkeys.txt"
DESCRIPTOR_TYPE = "wpkh" # "pkh" for legacy addresses, "wpkh" for Bech32/SegWit
RESCAN_TIMESTAMP = 0 # Unix timestamp 0 for full blockchain scan. Set e.g. to 1356998400 for Jan 1, 2013, or adjust to the timestamp of last import
BATCH_SIZE = 50

def is_scanning():
	try:
		output = subprocess.check_output([CLI_COMMAND, "getwalletinfo"]).decode("utf-8")
		info = json.loads(output)
		scanning = info.get("scanning", False)
		return scanning != False
	except Exception as e:
		print(f"Error checking wallet info: {e}")
		return True

def wait_for_rescan_complete():
	while is_scanning():
		print("Wallet is scanning; waiting 5 seconds...")
		time.sleep(5)

def main():
	if not os.path.exists(PRIVKEYS_FILE):
		print(f"Error: {PRIVKEYS_FILE} not found in the current directory.")
		sys.exit(1)

	with open(PRIVKEYS_FILE, "r") as f:
		keys = [line.strip() for line in f if line.strip()]

	total_keys = len(keys)
	if total_keys == 0:
		print(f"Error: No private keys found in {PRIVKEYS_FILE}.")
		sys.exit(1)

	current_batch = []
	for i, key in enumerate(keys):
		print(f"\n{i+1}/{total_keys}")

		desc_without_checksum = f"{DESCRIPTOR_TYPE}({key})"
		try:
			info_output = subprocess.check_output([CLI_COMMAND, "getdescriptorinfo", desc_without_checksum]).decode("utf-8")
			info = json.loads(info_output)
			checksum = info["checksum"]
			full_desc = f"{desc_without_checksum}#{checksum}"

			timestamp = RESCAN_TIMESTAMP if i == total_keys - 1 else "now"
			current_batch.append({
				"desc": full_desc,
				"timestamp": timestamp
			})

			if len(current_batch) == BATCH_SIZE or i == total_keys - 1:
				wait_for_rescan_complete()
				import_json = json.dumps(current_batch)
				subprocess.check_call([CLI_COMMAND, "importdescriptors", import_json])
				print(f"Imported batch of {len(current_batch)} keys.")
				current_batch = []

		except subprocess.CalledProcessError as e:
			print(f"Error running {CLI_COMMAND}: {e}")
			sys.exit(1)
		except json.JSONDecodeError:
			print("Error parsing JSON from getdescriptorinfo.")
			sys.exit(1)
		except KeyError:
			print("Checksum not found in descriptor info.")
			sys.exit(1)
		except Exception as e:
			print(f"Unexpected error for key {key[:5]}...: {e}")
			sys.exit(1)

	print("\n[INFO] All private keys imported successfully.\n\n")
	input("Press Enter to exit...")

if __name__ == "__main__":
	main()