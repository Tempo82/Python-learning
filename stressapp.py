# ------------------------------
# DIGITAL GARAGE SW TOOLS
# ------------------------------
# Python Stress Test APP
# DevLAB #onlyhardcore
# Created in homework sessions by tempo&brain 26'
# ------------------------------
# IMPORT LIBRARIES
# ------------------------------
import random
import time
import string
import csv
import os
import sys
# ------------------------------
# KONFIGURATION OF REQS/DELAY/CARS
# ------------------------------
NUM_REQUESTS = 50  # number of requests sent per car
DELAY = 0.1  # Pause between sent requests in (s)
MAX_CARS = 70  # number of simulated Cars in Stress Test 
# 
# ------------------------------
# SIMULATED CAR DEFINITION
# ------------------------------
class CarSimulator:
    def __init__(self, vin):
        self.vin = vin
        self.firmware = "v0"
        self.user_settings = {}
        self.speed = 0
        self.battery = 12.5
        self.gps_lat = 50.07
        self.gps_lon = 14.437
        self.engine_temp = 90
        self.rpm = 800

    def read_sensors(self):
        self.speed = round(random.uniform(0, 250), 1)
        self.battery = round(random.uniform(12.0, 14.8), 2)
        self.gps_lat = round(random.uniform(50.065, 50.085), 6)
        self.gps_lon = round(random.uniform(14.427, 14.447), 6)
        self.engine_temp = round(random.uniform(70, 105), 1)
        self.rpm = random.randint(600, 7000)
        return {
            "vin": self.vin,
            "speed": self.speed,
            "battery": self.battery,
            "gps_lat": self.gps_lat,
            "gps_lon": self.gps_lon,
            "engine_temp": self.engine_temp,
            "rpm": self.rpm,
            "firmware": self.firmware,
            "user_settings": self.user_settings,
        }

    def update_settings(self, data):
        self.firmware = data.get("firmware", self.firmware)
        self.user_settings.update(data.get("user_settings", {}))

# ------------------------------
# DEFINITIOM OF USED FUNCTIONS
# ------------------------------
def generate_vin():
    chars = string.ascii_uppercase.replace("I", "").replace("O", "") + string.digits
    return "".join(random.choices(chars, k=17))


def show_app_info():
    print("<=== Car Simulator Load Test APP ===>")
    print("Written in Python as homework session")
    print("               ")
    print("[INFO] Tento test simuluje komunikaci jednoho")
    print("či více vozidel s backendem. Sleduje zátěž,")
    print("latency, chyby a časování a stabilitu dat. Tento test")
    print("je důležitý k ověření spolehlivosti a výkonu")
    print("celého propojeného automotive systému před")
    print("jeho samotným nasazením do reálných vozidel.")


def wizard_select_test_type():
    print("    ")
    print("<=== Výběr typu testu ===>")
    print("1:OUT - Test backendu")
    print("2:INCAR - Test auta nebo hromadně flotily aut")
    choice = input("#Vyberte možnost (1/2): ").strip()
    if choice not in ["1", "2"]:
        print("[INFO] Neplatná volba, použije se default test backendu")
        choice = "1"
    return choice


def wizard_load_vins():
    print("    ")
    print("    ")
    print("<=== Výběr zadání VIN vozidla ===>")
    print("1: Použít pro test demo VIN")
    print("2: Zadání VIN ručně")
    print("3: Načíst hromadně čísla VIN aut ze souboru (CSV/TXT, 1 VIN na řádek)")
    choice = input("Zvolte možnost po (1/2/3): ").strip()
    vins = []

    if choice == "1":
        vins = ["DEMODEMO1234567890"]
    elif choice == "2":
        vin_input = input("Zadejte VIN (17 znaků): ").strip().upper()
        vins = [vin_input] if len(vin_input) == 17 else ["DEMODEMO1234567890"]
    elif choice == "3":
        file_path = input("Zadejte cestu k souboru: ").strip()
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                vins = [line.strip().upper() for line in f if len(line.strip()) == 17]
            if not vins:
                print("[INFO] Soubor neobsahuje validní VIN. Použiji demo VIN.")
                vins = ["DEMODEMO1234567890"]
        else:
            print("[INFO] Soubor s VIN nenalezen. Použiji demo VIN.")
            vins = ["DEMODEMO1234567890"]
    else:
        vins = ["DEMODEMO1234567890"]

    print(f"[INFO] Vybraná VIN: {vins}\n")
    return vins


def simulate_test(cars, test_type="backend"):
    print("      ")
    print(f"\n<=== Start vybraného testu číslo: {test_type} ===>\n")
    results = []

    for car in cars:
        for i in range(NUM_REQUESTS):
            start_time = time.time()
            data = car.read_sensors()
            car.update_settings(
                {"firmware": f"v{i}", "user_settings": {"mode": f"{test_type}_test"}}
            )
            latency = round(time.time() - start_time, 3)

# Simulation of Bug: latency > 0.05 s
            is_error = latency > 0.05

            results.append(
                {
                    "vin": car.vin,
                    "request_no": i,
                    "latency": latency,
                    "firmware": car.firmware,
                    "speed": data["speed"],
                    "battery": data["battery"],
                    "error": is_error,
                }
            )

# Results in text form monochromatic
            if is_error:
                print(
                    f"[ERROR] [{car.vin}] Req {i} | Firmware: {car.firmware} | "
                    f"Latency: {latency}s | Speed: {data['speed']} km/h | Battery: {data['battery']}V"
                )
            else:
                print(
                    f"[OK]    [{car.vin}] Req {i} | Firmware: {car.firmware} | "
                    f"Latency: {latency}s | Speed: {data['speed']} km/h | Battery: {data['battery']}V"
                )

            time.sleep(DELAY)
    return results


def print_summary(results):
    print("\n<=== Souhrn aktuálně dokončeného testu ===>")
    total = len(results)
    success = sum(1 for r in results if not r["error"])
    failed = sum(1 for r in results if r["error"])
    avg_latency = sum(r["latency"] for r in results) / total
    max_latency = max(r["latency"] for r in results)
    firmware_versions = set(r["firmware"] for r in results)

    print(f"Celkem requestů: {total}")
    print(f"Úspěšné: {success} | Chybné: {failed}")
    print(f"Firmware verze použitá v testu: {firmware_versions}")
    print(f"Průměrná latence: {round(avg_latency, 3)}s")
    print(f"Max latence: {max_latency}s")

# Detail of Bug
    if failed > 0:
        print("\n--- Detail chyb ---")
        for r in results:
            if r["error"]:
                print(
                    f"[{r['vin']}] Req {r['request_no']} | Latency: {r['latency']}s | "
                    f"Firmware: {r['firmware']} | Speed: {r['speed']} km/h | Battery: {r['battery']}V"
                )


# ------------------------------
# MAIN PROGRAM LOOP
# ------------------------------
if __name__ == "__main__":
    show_app_info()  # <<< Zobrazíme text hned po spuštění
    test_type = wizard_select_test_type()
    vins = wizard_load_vins()
    cars = [CarSimulator(vin) for vin in vins]

    # Adding of more cars in case it is a full stress tes - INCAR test
    if test_type == "2" and len(cars) < MAX_CARS:
        while len(cars) > MAX_CARS:
            cars.append(CarSimulator(generate_vin()))

    print(f"[INFO] Simulujeme aktuálně tento počet aut: {MAX_CARS:} aut\n")

    results = simulate_test(cars, test_type=test_type)

    print_summary(results)
    sys.exit(0)  

# END OF CODE/HELL STARTs HERE
