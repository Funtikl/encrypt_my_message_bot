from telegram.ext import *
from cryptography.fernet import Fernet
from api import API_KEY

API_KEY = API_KEY
print('bot işə başladı...')


generated = Fernet.generate_key()
print(generated)
def start_command(update, context):
    update.message.reply_text("""Generasiya olunmuş açarı yadda saxlayın.
    Açar = {}
    -------------------------------------------

    Mesaj yazaraq onun şifrələnmiş versiyasını əldə edin. Daha sonra isə:
    Şifrələnmiş mesajları oxumaq üçün yazın decrypt: və arxasıyca encrypt olunmuş dırnaq içində olan şifrəni yazın.
    """.format(generated))

def handle_message(update, context):
    text = update.message.text
    if not text.startswith("decrypt"):
        encoded_message = text.encode()
        print(encoded_message)
        f = Fernet(generated)
        encrypted_message = f.encrypt(encoded_message).decode()
        print(encrypted_message)
        update.message.reply_text({"mesaj":encrypted_message})
        update.message.reply_text("""Mesajı başqa birinin oxuması üçün, dırnaq içində olan şifrəni
        kopyalayıb -> https://8gwifi.org/fernet.jsp - saytında decrypt üçün istifadə etmək lazımdır.
        Açar sözü də qeyd etməyi unutmayın :)""" )
    else:
        text = text.replace('decrypt:','')
        text = text.replace(' ','')
        text = text.encode()
        print(text)
        f = Fernet(generated)
        print(generated)
        decryted_message = f.decrypt(text).decode()
        update.message.reply_text(decryted_message)

def decrypt_command(update,context):

    update.message.reply_text("Mesaja baxmaq üçün: https://8gwifi.org/fernet.jsp daxil olun, decrypt düyməsinə basın. Açarı və şifrələnmiş mesajı qeyd edin.")


def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("decrypt", decrypt_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling(1)
    updater.idle()
if __name__ == '__main__':
    main()