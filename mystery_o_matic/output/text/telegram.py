from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


class BufferStdout:
    last_output = ""

    def write(self, input):
        print(input)
        self.last_output += input

    def reset(self):
        self.last_output = ""

    def flush(self):
        pass


async def command(shell, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answer user message."""
    if update.message.text is None:
        return
    command = update.message.text.replace("/", "").lower()
    shell.onecmd(command)
    last_output = shell.stdout.last_output
    shell.stdout.reset()
    if last_output == "":
        return
    await update.message.reply_text(last_output)


def create_telegram_bot(shell, api_key):
    shell.stdout = BufferStdout()
    app = ApplicationBuilder().token(api_key).build()
    app.add_handler(MessageHandler(filters.ALL, (lambda u, c: command(shell, u, c))))
    return app
