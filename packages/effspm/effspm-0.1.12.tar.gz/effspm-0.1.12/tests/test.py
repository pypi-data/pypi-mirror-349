from effspm import BTMiner
import time

# === Parameters ===
data_path = "/Users/yeswanthvootla/Desktop/final_kosarak_s.txt"
min_support = 0.01         # float or int
time_limit = 36000         # seconds
preproc = True             # Enable preprocessing
use_dic = False            # Disable dictionary mapping
verbose = True            # Enable verbose logging
out_file = ""              # Keep empty unless you want file output

# === Run BTMiner ===
start_time = time.time()
result = BTMiner(data_path, min_support, time_limit, preproc, use_dic, verbose, out_file)
end_time = time.time()

# === Process Output ===
patterns = result["patterns"]
print(f"[BTMiner] Found {len(patterns)} patterns")
print("Patterns:", patterns)
print(f"Time taken: {end_time - start_time:.4f} seconds")
