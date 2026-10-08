import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router
from storage import load_all, save_all


# ==== HEALTH CHECK ДЛЯ RENDER ====
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# ==== ОСНОВНОЙ ЗАПУСК ====
async def main():
    print("🚀 Hotoci MuzBot запущен!", flush=True)

    load_all()

    threading.Thread(target=start_health_server, daemon=True).start()
    print(f"🏥 Health check на порту {os.getenv('PORT', 10000)}", flush=True)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        save_all()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
