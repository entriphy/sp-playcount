import asyncio
from app import App
from aiohttp import web
import os, socket

def find_available_port(start_port, end_port):
    for port in range(start_port, end_port + 1):
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Try binding to the port
                s.bind(('localhost', port))
                return port
        except OSError:
            # Port is already in use, continue to the next port
            pass

    # No available port found
    return None

async def main(event_loop: asyncio.AbstractEventLoop = None):
    app = App()
    await app.refresh_token()

    runner = web.AppRunner(app.app)
    await runner.setup()
    # port = find_available_port(5000, 8000)
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.getenv("PORT", 5001)))
    await site.start()
    print("Site running on port " + str(site._port))

    # This is broken
    while True:
        try:
            await asyncio.sleep(15 * 60)
            await app.refresh_token()
        except:
            await app.cleanup()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(loop))
