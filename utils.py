import time
from telegram import ChatAction, ParseMode
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name

def escape_reserved(raw):
    reserved = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    for r in reserved:
        raw = raw.replace(r, f"\\{r}")
    return raw


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def add_text_message(update, context, message):
    context.bot.send_message(
        chat_id=get_chat_id(update, context),
        text=message,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def check_confimation(update, context):
    add_text_message(update, context, escape_reserved("y/n?"))
    confirmation = update.message.text
    if confirmation == "y":
        add_text_message(update, context, "Confirmed...")
        return True
    else:
        add_text_message(update, context, "Exitting...")
        return False

def get_lexer(lang):
    try:
        return get_lexer_by_name(lang)
    except:
        return get_lexer_by_name("text")

def code_to_img(lang, code):
    return highlight(code, get_lexer(lang), ImageFormatter(style="perldoc"))
