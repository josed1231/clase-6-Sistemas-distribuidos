import asyncio

# Datos globales (El "Hotel")
habitaciones = 8
lock = asyncio.Lock()
semaforo = asyncio.Semaphore(5)

async def proceso_reserva(id_cliente):
    global habitaciones
    
    # El semáforo controla el flujo de entrada (Máximo 5 a la vez)
    async with semaforo:
        # El lock protege el dato para que no haya sobreventa
        async with lock:
            if habitaciones > 0:
                await asyncio.sleep(0.2) # Simula proceso lento
                habitaciones -= 1
                print(f"Cliente {id_cliente}: ¡Reserva exitosa!")
            else:
                print(f"Cliente {id_cliente}: Lo siento, no hay cupo.")

async def main():
    print(f"--- Iniciando reservas. Disponibles: {habitaciones} ---")
    
    # Creamos los 30 clientes
    tareas = [proceso_reserva(i) for i in range(1, 31)]
    
    # Ejecutamos todo
    await asyncio.gather(*tareas)
    
    print(f"--- Proceso terminado. Quedaron: {habitaciones} habitaciones ---")

if __name__ == "__main__":
    asyncio.run(main())