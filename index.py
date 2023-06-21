import asyncio
from app import App
from aiohttp import web

async def main(event_loop: asyncio.AbstractEventLoop):
    app = App()
    await app.refresh_token()

    runner = web.AppRunner(app.app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port=8080)
    await site.start()

    # This is broken
    while True:
        try:
            await asyncio.sleep(60)
        except:
            await app.cleanup()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(loop))
