import socketio,asyncio
a=['Processed_file', '2021-1-1_2021-12-31_without_profile.jsonl', 'Processed_percentage: 100%', 'Processed_lines:', 30404]
async def send_message_to_server(message):
    sio = socketio.AsyncClient()

    @sio.on('connect')
    async def on_connect():
        print('Connected to server')
        await sio.emit('message_from_client', {'message': message})
        print("Message sent.")

    await sio.connect('http://')
    #     await sio.wait()  # Waiting for all tasks to complete (if there's any event listener running)
    # finally:
    await sio.disconnect()
# 使用示例:
while True:
    asyncio.run(send_message_to_server(input("input:")))
