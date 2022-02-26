from utils import (
    code_to_img,
    get_chat_id,
)

def help_command_handler(update, context):
    update.message.reply_text(
        "Convert code to syntax highlighted image!\nStart with `/code` and specify the language, and finally write your code from the next line onwards. \n\nExample:\n/code python\nprint('hello')\n\n"
    )

def code_command_handler(update, context):
    if not context.args:
        update.message.reply_text("Please provide a code snippet")
        return
    if context.args[0] == "@codetoimg_bot":
        lang = context.args[1]
    else:
        lang = context.args[0]
    code = "\n".join(update.message.text.split("\n")[1:])
    try:
        context.bot.send_photo(
            chat_id=get_chat_id(update, context), photo=code_to_img(lang, code)
        )
    except Exception as e:
        print(e)
