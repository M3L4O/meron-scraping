import json


def clear_cpu(cpu, cpu_detail):
    return {
        "manufacturer": cpu_detail.get("Manufacturer", ""),
        "model": cpu["model"],
        "socket": cpu_detail.get("Socket", ""),
        "n_cores": int(cpu_detail.get("Core Count", 0)),
        "base_clock_spd": cpu_detail.get("Performance Core Clock", ""),
        "boost_clock_spd": cpu_detail.get("Performance Core Boost Clock", ""),
        "consumption": int(cpu_detail.get("TDP", "").split()[0]),
        "integrated_gpu": cpu_detail.get("Integrated Graphics", ""),
    }


def clear_gpu(gpu):
    return {
        "manufacturer": gpu.get("model", "").split()[0],
        "model": gpu.get("model", ""),
        "consumption": gpu.get("TDP", ""),
        "vram": gpu.get("Memory", ""),
        "vram_spd": gpu.get("Core Clock", ""),
    }


def clean_motherboard(mobo, mobo_detail):
    return {
        "manufacturer": mobo_detail.get("Manufacturer", ""),
        "model": mobo["model"],
        "socket": mobo_detail.get("Socket / CPU", ""),
        "board_size": mobo_detail.get("Form Factor", ""),
        "n_ram_slots": int(mobo_detail.get("Memory Slots", 0)),
        "Memory Type": mobo_detail.get("Memory Type", ""),
        "Memory Capacity": (
            float(mobo_detail.get("Memory Max", "0").replace(" GB", ""))
            if "Memory Max" in mobo_detail
            else 0.0
        ),
        "Supported Ramspeeds": mobo_detail.get("Memory Speed", None),
        "SATA": mobo_detail.get("SATA 6.0 Gb/s Ports", None),
        "M.2 ": len(mobo_detail.get("M.2 Slots", [])),
        "PCI-E x1": int(mobo_detail.get("PCIe x1 Slots", 0)),
        "PCI-E x4": int(mobo_detail.get("PCIe x4 Slots", 0)),
        "PCI-E x8": int(mobo_detail.get("PCIe x8 Slots", 0)),
        "PCI-E x16": int(mobo_detail.get("PCIe x16 Slots", 0)),
        "USB 3 Headers": len(
            [
                h
                for h in [
                    mobo_detail.get("USB 3.2 Gen 1 Headers"),
                    mobo_detail.get("USB 3.2 Gen 2 Headers"),
                ]
                if h
            ]
        ),
    }


def clear_ram(ram):
    return {
        "manufacturer": ram.get("model", "").split()[0],
        "model": ram.get("model", ""),
        "generation": ram.get("Speed", "").split("-")[0],
        "size": (
            ram.get("Modules", "").split("x")[-1].strip() if "Modules" in ram else ""
        ),
        "frequency": int(ram.get("Speed", "").split("-")[1]),
    }

    # {
    #     "Capacity": "2 TB",
    #     "Price / GB": "$0.085",
    #     "Type": "SSD",
    #     "Cache": "2048 MB",
    #     "Form Factor": "M.2-2280",
    #     "Interface": "M.2 PCIe 4.0 X4",
    #     "model": "Samsung 990 Pro",
    #     "uri": "/product/34ytt6/samsung-990-pro-2-tb-m2-2280-pcie-40-x4-nvme-solid-state-drive-mz-v9p2t0bw"
    # },
    # {
    #     "manufacturer":"Crucial",
    #     "model":"Crucial P2 1000 GB",
    #     "storage":"1000 GB",
    #     "io":"NVM"
    # },
    # {
    #     "manufacturer":"HGST",
    #     "model":"HGST Deskstar NAS 0S03661",
    #     "storage":"3 TB",
    #     "rpm":7200.0
    # },


def clear_storage(storage):
    return {
        "manufacturer": storage.get("model", "").split()[0],
        "model": storage.get("model", ""),
        "capacity": storage.get("Capacity"),
        "io": storage.get("Interface"),
        "type": storage.get("Type") if "RPM" not in storage.get("Type") else "HDD",
        "rpm": storage.get("Type") if "RPM" in storage.get("Type") else None,
    }


def clean_psu(psu):
    return {
        "manufacturer": psu.get("model", "").split()[0],
        "model": psu.get("model", ""),
        "power": int(psu.get("Wattage", "0 W").replace(" W", "")),
        "rate": psu.get("Efficiency Rating", ""),
    }


components = {
    # "cpu": (["data/cpu.json", "data/cpu_detail.json"], clear_cpu),
    # "gpu": ("data/gpu.json", clear_gpu),
    "motherboard": (["data/motherboard.json","data/motherboard_detail.json"], clean_motherboard),
    # "ram": ("data/ram.json", clear_ram),
    # "storage": ("data/storage.json", clear_storage),
    # "psu": ("data/psu.json", clean_psu),
}


for key, value in components.items():
    path, func = value

    if type(path) is list:
        shallow, detail = path

        with open(detail, "r") as file:
            detail_specs = json.load(file)

        with open(shallow, "r") as file:
            shallow_specs = json.load(file)[: len(detail_specs)]

        print(f"{len(shallow_specs)=}: {len(detail_specs)=}")

        components_clear_specs = list(map(func, shallow_specs, detail_specs))

    else:
        with open(path, "r") as file:
            components_specs = json.load(file)

        components_clear_specs = list(map(func, components_specs))

    with open(f"data/{key}_clean.json", "w") as file:
        json.dump(components_clear_specs, file, indent=4, ensure_ascii=False)
