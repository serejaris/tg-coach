import logging

from telegram.ext import ApplicationBuilder

from bot.config import load_config
from bot.database import create_pool, create_tables
from bot.handlers import register_handlers
from bot.scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application):
    config = application.bot_data["config"]
    pool = await create_pool(config.database_url)
    application.bot_data["db_pool"] = pool
    await create_tables(pool)

    register_handlers(application)
    setup_scheduler(application)

    if config.admin_chat_id:
        await application.bot.send_message(
            chat_id=config.admin_chat_id,
            text="\U0001f7e2 IdeaCatcher launched",
        )
    logger.info("Bot initialized, DB connected")


async def post_shutdown(application):
    pool = application.bot_data.get("db_pool")
    if pool:
        await pool.close()
        logger.info("DB pool closed")


def main():
    config = load_config()
    app = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    app.bot_data["config"] = config
    app.run_polling()


if __name__ == "__main__":
    main()
