from fastapi import FastAPI
import asyncio

app = FastAPI()

# Empezamos con 8 habitaciones
habitaciones_disponibles = 8
# El candado para que no se crucen las reservas
lock = asyncio.Lock()

@app.get("/reservar")
async def reservar():
    global habitaciones_disponibles
    
    # El lock asegura que solo un cliente revise y reste a la vez
    async with lock:
        if habitaciones_disponibles > 0:
            # Simulamos el tiempo de proceso
            await asyncio.sleep(0.2)
            habitaciones_disponibles -= 1
            return {"mensaje": "¡Reservado!"}
        else:
            return {"mensaje": "Sin disponibilidad"}

@app.get("/estado")
async def estado():
    return {"disponibles": habitaciones_disponibles}

@app.post("/reiniciar")
async def reiniciar():
    global habitaciones_disponibles
    async with lock:
        habitaciones_disponibles = 8
    return {"mensaje": "Reiniciado a 8 habitaciones"}