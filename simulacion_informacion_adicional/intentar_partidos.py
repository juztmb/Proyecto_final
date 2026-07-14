"""import http.client

conn = http.client.HTTPSConnection("https://api.kickoffapi.com/api/v1")

headers = {
    'x-apisports-key': "ft_dev_856953ea12addaa0c2f6d964474ddaa13509efe5"
    }

conn.request("GET", "/leagues", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))"""


import http.client
import json
import asyncio
import aiohttp

# CORRECCIÓN: Pasa solo el dominio sin el protocolo




async def enviar_datos(url: str, datos: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=datos) as response:
            status = response.status
            resultado = await response.json()  # o .text() si no responde JSON
            return status, resultado

async def main():
    url = "http://127.0.0.1:8000/partido/create"
    #conn = http.client.HTTPSConnection("api.zafronix.com")

    #headers = {
        #"X-API-Key": "zwc_free_27026a41d81306144368c4d4"
    #}

    # El resto de tu código se queda exactamente igual
    #conn.request("GET", "/fifa/worldcup/v1/teams?tournament=2026", headers=headers)
    #response = conn.getresponse()
    with open('Mexico_partido.JSON','r',encoding='utf-8') as f:
        datos = json.load(f)


    for player in datos:
        status, resultado = await enviar_datos(url, player)
        print(f"Código de estado: {status}")
        print(f"Respuesta: {resultado}")

if __name__ == "__main__":
    asyncio.run(main())
                
            



    '''
        { "_id": "2020245",
        "nombre": "Mbappe",
        "equipo": "Francia",
        "numero_camiseta": "54",
        "precio":152.42,
        "puntos_jugador": 0,
        "tarjetas":{
            "amarilla":0,
            "roja": 0
        },
        "goles":0,
        "asistencias":0,
        "remates_arco":0,
        "posicion": "Delantero"
        }
    '''

    #2026215 Quiñones, must have 1 gol
    #2026202 Deberia tener una tarjeta amarilla
    #y puntos en los 3 teams deben cambiar 