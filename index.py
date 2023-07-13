import asyncio
from app import App
from aiohttp import web
import os


async def main(event_loop: asyncio.AbstractEventLoop = None):
    app = App()
    await app.refresh_token()

    runner = web.AppRunner(app.app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=int(os.getenv("PORT", 5050)))
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
