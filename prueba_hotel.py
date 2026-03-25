import asyncio
import httpx

# El semáforo deja pasar a 5 personas a la vez
semaforo = asyncio.Semaphore(5)

async def hacer_reserva(numero_cliente, cliente_http):
    # Hacemos fila con el semáforo
    async with semaforo:
        try:
            respuesta = await cliente_http.get("http://127.0.0.1:8000/reservar")
            datos = respuesta.json()
            print(f"Cliente {numero_cliente}: {datos['mensaje']}")
        except Exception as e:
            print(f"Cliente {numero_cliente}: Error al conectar")

async def main():
    # Primero reiniciamos para empezar en limpio con 8 habitaciones
    async with httpx.AsyncClient() as cliente_http:
        await cliente_http.post("http://127.0.0.1:8000/reiniciar")

    # Lanzamos las 30 peticiones
    async with httpx.AsyncClient(timeout=15.0) as cliente_http:
        # Preparamos a los 30 clientes
        tareas = [hacer_reserva(i, cliente_http) for i in range(1, 31)]
        # Los mandamos todos a la vez
        await asyncio.gather(*tareas)

    # Consultamos cómo quedó todo al final
    async with httpx.AsyncClient() as cliente_http:
        respuesta_final = await cliente_http.get("http://127.0.0.1:8000/estado")
        datos = respuesta_final.json()
        print(f"\nHabitaciones disponibles al final: {datos['disponibles']}")

asyncio.run(main())