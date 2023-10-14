import socketio,asyncio

async def send_message_to_server(message):
    sio = socketio.AsyncClient()

    @sio.on('connect')
    async def on_connect():
        print('Connected to server')
        await sio.emit('message_from_client', {'message': message})
        print("Message sent.")

    await sio.connect('http://129.159.198.118:5000')

# 使用示例:
while True:
    asyncio.run(send_message_to_server(input("input:")))
