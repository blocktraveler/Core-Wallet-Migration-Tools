 ##################################################################################
 ##                                                                              ##
 ##                        Core Wallet Migration Tools                           ##
 ##                                                                              ##
 ##           Website: www.namecoin.pro | Web3 ID: https://dotbit.app            ##
 ##                                                                              ##
 ##################################################################################

====================================================================================

  Overview
  
====================================================================================

  These platform independent wallet migration tools facilitate the migration of 
  private keys from legacy Berkeley DB (BDB) wallets to modern descriptor wallets 
  in Bitcoin and Namecoin Core. Place the tools in the folders (e.g. on Windows):

      C:\Program Files\Bitcoin\daemon
      C:\Program Files\Namecoin\daemon

  Included Scripts:
  -----------------
  1. Dump_privkeys.py  - Export private keys of names and UTXOs.
  2. Import_descriptors.py  - Import private keys into descriptor wallets.

  Prerequisites:
  -----------------
  * Download and install Python from https://www.python.org/downloads/
  * Configure RPC credentials

	On a fresh installation create (otherwise edit) the file "bitcoin.conf" (for Bitcoin) resp.
    "namecoin.conf" (for Namecoin) in the data directory with minimal content:

		server=1
		rpcallowip=127.0.0.1
		rpcbind=127.0.0.1
		rpccookiefile=.\.cookie
        fallbackfee=0.0002

    This minimal configuration uses cookie authentication to be used on the local machine. The
    parameter "fallbackfee" is a recommended setting for the transaction fee calculation (value
    '0.0002' NMC for Namecoin).
    
    You can also just copy the configuration file predefined in this package.

	Data directory locations (e.g. for Namecoin):

		Windows:
		_______

			%AppData%\Namecoin


		macOS (enable visibility with 'command chflags nohidden ~/Library' in the terminal before):
		___________________________________________________________________________________________

			~/Library/Application Support/Namecoin/


		Linux:
		______

			$HOME/.namecoin/

====================================================================================

  Dump_privkeys.py
  
====================================================================================

  This Python script automates the extraction of private keys for:
    1. Unspent Transaction Outputs (UTXOs) using the 'listunspent' RPC command.
    2. Names (assets) held in your wallet using the 'name_list' RPC command (Namecoin only).

  Known Issues (Namecoin only):
  -----------------------------
  - If two consecutive name updates to different addresses were made at the same block,
    the 'name_list' RPC command will incorrectly output the first (invalid) private key.
    In such cases:
      - Manually export the correct private key using the 'dumpprivkey' RPC command.

  Prerequisites:
  --------------
  - Define Bitcoin or Namecoin Core (bitcoin-cli or namecoin-cli) at line 13.
  - Ensure the wallet is unlocked if encrypted.
  - Wait until all your wallet transactions have at least one confirmation to include all UTXOs.
  - The script assumes you are using a legacy Berkeley DB (BDB) wallet in Bitcoin or Namecoin Core.
  - Make sure the Core wallet is running and the RPC access is properly configured.

  Notes:
  ------
  - The extracted private keys should be handled with extreme caution.
    Never share or expose them, as they grant access to your funds and assets!
  - This script does not modify wallet data; it only exports private keys for 
    backup and migration purposes.

  Output:
  -------
  - Private keys for names and UTXOs will be stored line by line in the 'privkeys.txt'. 
  - Rename or backup previous 'privkeys.txt' files.

====================================================================================

  Import_descriptors.py
  
====================================================================================

  This Python script automates the process of importing private keys from 
  legacy Berkeley DB (BDB) wallets in Bitcoin and Namecoin Core (stored line by line in the 
  'privkeys.txt') into modern descriptor wallets in Bitcoin and Namecoin Core. It automatically
  detects the key type for the Bitcoin and Namecoin mainnet (Bech32 or Base58Check).

  Additional Notes:
  -----------------
  - Define Bitcoin or Namecoin Core (bitcoin-cli or namecoin-cli) at line 13. 
  - Private keys must be exported from BDB wallets in Bitcoin or Namecoin Core using 
    'Dump_privkeys.py' or via the RPC command 'dumpprivkey'.
  - Ensure the wallet is unlocked if encrypted.
  - All descriptors are imported in batches of 50 descriptors, otherwise larger 
    wallets might exceed the maximum command size.
  - Wait at least 15 blocks (two hours) after your last wallet transactions to avoid 
    a rescan of the most recent transactions during each batch import.
  - By default, a full blockchain rescan is initiated on the last import. Depending on
    the size of your wallet, this may cause a timeout error on the last import, which
    can be ignored as it won't affect a successful import.
  - Set Unix timestamp at line 15 e.g. to 1356998400 for Jan 1, 2013 (or to the
    timestamp of your last import), dependent on the age of the asset to import.
  - For multi-signature addresses (both legacy and Bech32), modifications to the 
    script are required.

====================================================================================

  IMPORTANT: Handle all private keys and descriptors with caution! Mishandling them 
  may result in the loss of funds or assets. Use these tools responsibly.
  
====================================================================================

  DISCLAIMER: These scripts are provided "as is" without warranty of any kind,
  either expressed or implied. The author disclaims any responsibility or liability
  for any loss of funds, assets or data, or for any damage resulting
  from its use or misuse!
  
====================================================================================

