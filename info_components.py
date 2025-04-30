import json

from glob import glob

total = 0
for filename in glob("data/*_clean.json"):
    print(filename)
    with open(filename, "r") as file:
        components = json.load(file)
        print("Tipo de componente: " + filename.split(".")[0].split("_")[0])
        print(f"Quantidade: {len(components)}")
        print(f"Informações: {list(components[0].keys())}")
        print("\n\n")
        total += len(components)
    
print(f"Total: {total}")