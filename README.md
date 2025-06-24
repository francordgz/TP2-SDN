# TP N° 2: Software-Defined Networks
---
## Requisitos
- Python 3.x
- Herramientas para análisis de redes: Mininet, Wireshark, iperf
- Ejecutar en ambiente UNIX (opcional, pero recomendado)

Por si no cuenta con alguna dependencia, puede instalarla según lo establecido en la siguiente sección.

## Instalación de dependencias
- Si no está en ambiente UNIX, dirigirse a https://www.python.org/downloads/ y descargar e instalar la última versión estable. Caso contrario, debería tenerlo instalado por defecto en su sistema. Si tiene más problemas, ejecute `sudo apt-get update` seguido de `sudo apt-get install python3.x`, siendo "x" la que corresponda a la última estable
- `pip install flake8`: para verificar que el formato del código es correcto

## Instrucciones

A continuación se describen los pasos necesarios para probar el proyecto.
Asegúrese de ejecutar todos los comandos desde el directorio raíz del repositorio.

### 1. Ejecutar el firewall

Crear un enlace simbólico dentro de `src/pox/` que apunte al archivo original de nuestro firewall, para que POX pueda usar este módulo:

```bash
ln -s ../firewall.py src/pox/firewall.py
```

Luego, ejecuta POX con el módulo `firewall`:

```bash
python3 src/pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall
```

### 2. Ejecutar la topología personalizada

Para ejecutar la topología definida, usar el siguiente comando:

```bash
sudo mn --custom src/topology.py --topo customTopo,cantidad_switches=N --controller=remote --mac --arp --switch ovsk
```

Siendo `N >= 1` la **cantidad de switches**, donde `N >= 1`.

### 3. Configurar el firewall en un switch específico

Si se desea aplicar reglas de firewall a un switch en particular de la topología, **debe modificarse la siguiente constante en el archivo `src/firewall.py`**:

```python
DPID_FIREWALL_SWITCH = 1
```

El valor de dicha constante debe ser un valor entero entre `1` y `N` (el `N` elegido para la topología).