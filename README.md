# TP N° 2: Software-Defined Networks
---
## Requisitos
- Python 3.x
- Herramientas para análisis de redes: Mininet, Wireshark, iperf, POX, xterm
- Ejecutar en ambiente UNIX (opcional, pero recomendado)

Por si no cuenta con alguna dependencia, puede instalarla según lo establecido en la siguiente sección.

## Instalación de dependencias

- Si no está en ambiente UNIX, dirigirse a https://www.python.org/downloads/ y descargar e instalar la última versión estable. Caso contrario, debería tenerlo instalado por defecto en su sistema. Si tiene más problemas, ejecute `sudo apt-get update` seguido de `sudo apt-get install python3.x`, siendo "x" la que corresponda a la última estable

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

Siendo `N` la **cantidad de switches**, donde `N >= 1`.

### 3. Configurar el firewall en un switch específico

Si se desea aplicar reglas de firewall a un switch en particular de la topología, **debe modificarse la siguiente constante en el archivo `src/firewall.py`**:

```python
DPID_FIREWALL_SWITCH = 1
```

El valor de dicha constante debe ser un valor entero entre `1` y `N` (el `N` elegido para la topología).

## Correr las reglas establecidas

Para correr las siguientes reglas, ejecute el programa `xterm` dentro de la terminal de Mininet que quedó abierta luego de iniciar la topología con el módulo `firewall`.

Desde el prompt de Mininet, utilice el siguiente comando:

```bash
mininet> xterm hx hy
```

Donde `hx` y `hy` son los nombres de los hosts que participarán en una determinada regla.

En cada regla será indicado:

- Qué hosts deben abrirse con `xterm`.
- Qué comandos deben ejecutarse en las terminales de esos hosts.
        
## Reglas

El formato de los comandos para las reglas es el siguiente:

**Servidor**:

        iperf -s -p [port]

**Cliente**:

        iperf -c [dst_host] -p [port]

- **Regla 1**: Descartar mensajes con puerto destino 80  

        h2: iperf -u -s -p 80
        h1: iperf -u -c 10.0.0.2 -p 80 
    
    Para que los mensajes lleguen correctamente utilizar otro puerto.

- **Regla 2**: Descartar mensajes desde el host 1 al puerto 5001 usando UDP  

        h4: iperf -u -s -p 5001 
        h1: iperf -u -c 10.0.0.4 -p 5001

    Para que los mensajes lleguen correctamente utilizar otro puerto.

- **Regla 3**: Bloqueo de comunicacion entre 2 hosts (por ejemplo entre host1 y host3)

        h1: iperf -u -c 10.0.0.3 -p 10000
        h3: iperf -s -p 10000
