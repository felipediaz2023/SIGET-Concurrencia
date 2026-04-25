import threading
import time
import random
from queue import Queue
from threading import Semaphore, Lock

# Configuración
BUFFER_SIZE = 5
NUM_PRODUCTORES = 2
NUM_CONSUMIDORES = 2
DATOS_A_GENERAR = 10

# Recursos compartidos
buffer = Queue(BUFFER_SIZE)
mutex = Lock()

# Semáforos
espacios_disponibles = Semaphore(BUFFER_SIZE)
elementos_disponibles = Semaphore(0)

def productor(id_productor):
    for i in range(DATOS_A_GENERAR):
        time.sleep(random.uniform(0.5, 1.5))  # Simula lectura del sensor
        
        dato_trafico = f"Sensor {id_productor} → Vehículos: {random.randint(10, 100)}"
        
        espacios_disponibles.acquire()    # Espera si el buffer está lleno
        with mutex:                        # Exclusión mutua
            buffer.put(dato_trafico)
            print(f"[PRODUCTOR {id_productor}] Produjo: {dato_trafico}")
        elementos_disponibles.release()   # Señala que hay un nuevo dato

def consumidor(id_consumidor):
    for _ in range(DATOS_A_GENERAR):
        elementos_disponibles.acquire()   # Espera si el buffer está vacío
        with mutex:                        # Exclusión mutua
            dato = buffer.get()
            print(f"    [CONSUMIDOR {id_consumidor}] Procesó: {dato}")
        espacios_disponibles.release()    # Libera espacio en el buffer
        
        time.sleep(random.uniform(1, 2))  # Simula análisis del dato

# Crear hilos
productores = []
consumidores = []

for i in range(NUM_PRODUCTORES):
    p = threading.Thread(target=productor, args=(i+1,))
    productores.append(p)

for i in range(NUM_CONSUMIDORES):
    c = threading.Thread(target=consumidor, args=(i+1,))
    consumidores.append(c)

# Iniciar ejecución
for p in productores:
    p.start()

for c in consumidores:
    c.start()

# Esperar a que terminen
for p in productores:
    p.join()

for c in consumidores:
    c.join()

print("\n✅ Simulación SIGET finalizada sin condiciones de carrera ni bloqueos.")