# 🔎 FINGERPRINTER

**FINGERPRINTER** es una herramienta desarrollada en Python para realizar tareas básicas de **descubrimiento y reconocimiento de dispositivos dentro de una red IPv4 local**.

El programa detecta las redes disponibles en el equipo, permite seleccionar una de ellas y utiliza **Nmap, ARP y Scapy** para identificar hosts activos y obtener información básica de los dispositivos.

---

## ✨ Características

* 🔍 Detección automática de interfaces de red IPv4.
* 🌐 Identificación de las redes asociadas a cada interfaz.
* 📡 Descubrimiento de hosts activos mediante Nmap.
* 🖥️ Obtención de direcciones MAC mediante ARP.
* 🏭 Consulta del fabricante del dispositivo cuando Nmap proporciona esa información.
* 💻 Detección del sistema operativo mediante Nmap.
* 🔌 Enumeración de puertos TCP.
* 🛠️ Identificación básica de servicios.
* 🎨 Interfaz de consola coloreada mediante Colorama.
* 📊 Presentación de resultados mediante tablas de Rich.
* 🖼️ Banner personalizado mediante PyFiglet.
* ⚠️ Manejo básico de errores e interrupciones.

---

## 🧰 Tecnologías utilizadas

| Tecnología  | Uso                                          |
| ----------- | -------------------------------------------- |
| Python      | Lenguaje principal                           |
| Nmap        | Descubrimiento y reconocimiento de hosts     |
| Scapy       | Solicitudes ARP y obtención de MAC           |
| Psutil      | Obtención de interfaces y direcciones de red |
| IPaddress   | Manipulación y validación de redes IPv4      |
| Rich        | Presentación de resultados en tablas         |
| Colorama    | Colores en la terminal                       |
| PyFiglet    | Generación del banner                        |
| python-nmap | Interfaz de Python para Nmap                 |

---

## 📋 Requisitos

Antes de ejecutar el programa necesitas tener instalado:

* Python 3
* Nmap
* Permisos suficientes para realizar solicitudes ARP y determinadas funciones de reconocimiento.

### Dependencias de Python

Instala las dependencias mediante:

```bash
pip install colorama scapy rich python-nmap psutil pyfiglet
```

También puedes crear un archivo `requirements.txt`:

```text
colorama
scapy
rich
python-nmap
psutil
pyfiglet
```

Y posteriormente instalar todo con:

```bash
pip install -r requirements.txt
```

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

### 2. Entrar al directorio

```bash
cd FINGERPRINTER
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar Nmap

Comprueba que Nmap esté disponible desde la terminal:

```bash
nmap --version
```

Si el comando no es reconocido, debes instalar Nmap y asegurarte de que se encuentre disponible en el `PATH` del sistema.

---

## 🚀 Uso

Ejecuta el script:

```bash
python fingerprinter.py
```

Al iniciar, el programa mostrará un banner similar a:

```text
    FINGERPRINTER
```

Después buscará las redes IPv4 disponibles en el equipo.

Por ejemplo:

```text
[*] Looking up for all networks...

[*] Showing all results...

[1] Ethernet                       | 192.168.1.0/24
[2] Wi-Fi                          | 10.0.0.0/24

[*] Select a network to scan:
```

Selecciona el número correspondiente a la red que deseas analizar.

---

## 🔎 Descubrimiento de hosts

Después de seleccionar una red, el programa utiliza Nmap con:

```bash
nmap -sn <RED>
```

La opción `-sn` realiza un descubrimiento de hosts sin realizar un escaneo de puertos completo.

Los hosts encontrados se almacenan mediante:

```python
ALL_HOSTS = nm.all_hosts()
```

---

## 📡 Obtención de direcciones MAC

Para cada host detectado se genera una solicitud ARP utilizando Scapy:

```python
packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
    op="who-has",
    pdst=ip
)
```

La respuesta permite obtener la dirección MAC del dispositivo.

Los resultados se presentan en una tabla:

```text
==== ALL RESULTS ====

IP ADDRESS       MAC
192.168.1.1      XX:XX:XX:XX:XX:XX
192.168.1.10     XX:XX:XX:XX:XX:XX
192.168.1.20     XX:XX:XX:XX:XX:XX
```

---

## 🎯 Información del objetivo

Después de mostrar los hosts encontrados, el programa solicita una dirección IP:

```text
[*] IP TARGET:
```

La IP introducida se valida utilizando `ipaddress.IPv4Address`.

También se verifica que pertenezca a la red seleccionada.

Posteriormente se realiza un escaneo mediante Nmap:

```bash
nmap -sV -O --host-timeout 30s --max-retries 1 <IP>
```

### Información obtenida

Dependiendo de lo que el dispositivo permita detectar, el programa puede mostrar:

### IP

```text
IP ADDRESS: 192.168.1.10
```

### MAC

```text
MAC: XX:XX:XX:XX:XX:XX
```

### Fabricante

```text
MANUFACTURER: {...}
```

### Sistema operativo

```text
OS: Linux
```

### Puertos TCP

```text
Port: 22
    | State: open
    | Service: ssh

Port: 80
    | State: open
    | Service: http
```

La información disponible depende del dispositivo, de la red y de los permisos con los que se ejecute Nmap.

---

## 🧩 Funcionamiento del programa

El flujo principal del programa puede resumirse de la siguiente manera:

```text
                ┌──────────────────────┐
                │       Inicio         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Detectar interfaces  │
                │      IPv4            │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Mostrar redes        │
                │     disponibles      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Seleccionar red      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Nmap -sn             │
                │ Descubrir hosts      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ ARP / Scapy          │
                │ Obtener MAC          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Mostrar resultados   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Seleccionar objetivo │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Nmap -sV -O          │
                │ Fingerprinting       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Mostrar información  │
                └──────────────────────┘
```

---

## 📁 Estructura recomendada

Una estructura sencilla para el proyecto sería:

```text
FINGERPRINTER/
│
├── fingerprinter.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## ⚠️ Consideraciones

La herramienta está orientada al **reconocimiento de redes y dispositivos sobre los que tengas autorización para realizar pruebas**.

Algunas funciones pueden requerir privilegios elevados, especialmente aquellas relacionadas con ARP y detección del sistema operativo.

Además, la información obtenida por Nmap no siempre será completa. Por ejemplo, un dispositivo puede no proporcionar información suficiente para determinar con precisión su sistema operativo o fabricante.

---

## 🛡️ Uso responsable

Utiliza FINGERPRINTER únicamente en redes y dispositivos propios o en entornos donde tengas autorización para realizar análisis.

El objetivo de la herramienta es facilitar el aprendizaje de conceptos relacionados con:

* Redes IPv4
* ARP
* Direcciones MAC
* Descubrimiento de hosts
* Nmap
* Fingerprinting
* Enumeración de servicios
* Automatización con Python

---

## 📚 Conceptos relacionados

Este proyecto permite practicar conceptos de redes como:

**ARP → MAC → IP → Host Discovery → Port Scanning → Service Detection → OS Detection**

También permite comprender cómo diferentes herramientas pueden combinarse para realizar un proceso básico de reconocimiento de una red.

---

## 👨‍💻 Autor
Utrilla Solis, Angel
Desarrollado como proyecto de aprendizaje en Python y redes informáticas.

**FINGERPRINTER — Network Discovery & Fingerprinting Tool**
