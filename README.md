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

Desde el directorio raíz del proyecto, crea un enlace simbólico dentro de `src/pox/` que apunte al archivo original, para que POX pueda usar este módulo:

```bash
ln -s ../firewall.py src/pox/firewall.py
```

Ejecuta POX con el módulo firewall:

```bash
python3 src/pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall
```
