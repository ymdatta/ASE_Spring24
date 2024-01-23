import subprocess

print("Results for soybean.csv dataset")
print("______________________________")
print("|   k   |   m   |   Accuracy |")
print("______________________________")

for k in [0, 1, 2, 3]:
    for m in [0, 1, 2, 3]:
        command = f"python3 ../../src/gate.py -f ../../data/soybean.csv -k {k} -m {m}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        accuracy_line = [line for line in result.stdout.split('\n') if len(line) > 0]
        accuracy = float(accuracy_line[0].split()[-1]) if accuracy_line else None
        accuracy_str = f"{accuracy:.2f}%" if accuracy is not None else "N/A   "
        print(f"|   {k}   |   {m}   |   {accuracy_str}   |")
