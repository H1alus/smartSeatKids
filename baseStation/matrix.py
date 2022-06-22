import asyncio
import time
from nio import AsyncClient
from config import Config
import logging

CONNECTED_MESSAGE = "smart-seat connesso"
ALERT_MESSAGE = 'ATTENZIONE: BAMBINO ANCORA IN AUTO'

async def send_alert(client, room_id, message):
    logging.info(f'sending alert "{message}"' )
    return await client.room_send(
            room_id = room_id, 
            message_type = "m.room.message",
            content = {
                "msgtype" : "m.text",
                "body" : message
                }
            )

async def matrix_thread(active, alert):
    logging.info('started communication thread')
    conf = Config()
    client = AsyncClient(conf.home_server, conf.username)
    try:
        response = await client.login(conf.passwd)
    except:
        logging.error(response)
    

    while True:
        if active.is_set():
            await send_alert(client, conf.room_id, CONNECTED_MESSAGE)
            active.clear()

        if alert.is_set():
            await send_alert(client, conf.room_id, ALERT_MESSAGE)
        time.sleep(1)
