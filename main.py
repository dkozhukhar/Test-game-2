from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Опис простого ігрового світу: кожна локація має опис та доступні напрямки.
game_world = {
    "start": {
        "description": "Ви на початку своєї подорожі.",
        "exits": {"north": "forest", "east": "lake"}
    },
    "forest": {
        "description": "Ви опинилися у темному лісі.",
        "exits": {"south": "start"}
    },
    "lake": {
        "description": "Ви знаходитесь біля тихого озера.",
        "exits": {"west": "start"}
    }
}

# Для простоти зберігаємо поточну позицію одного користувача глобально.
current_room = "start"

@app.route('/')
def home():
    global current_room
    room = game_world[current_room]
    response = f"Ви знаходитесь у кімнаті: {current_room}. {room['description']}\n"
    response += "Доступні напрямки: " + ", ".join(room["exits"].keys())
    response += "\n\nДля переміщення використовуйте: /move?direction=<напрямок>"
    return response

@app.route('/move')
def move():
    global current_room
    direction = request.args.get("direction", "").lower()
    if direction in game_world[current_room]["exits"]:
        current_room = game_world[current_room]["exits"][direction]
        return redirect(url_for('home'))
    else:
        return f"Невірний напрямок: {direction}. Спробуйте ще раз. <a href='/'>Повернутись</a>"

if __name__ == '__main__':
    # Render очікує, що сервер слухатиме на 0.0.0.0 та порті, заданому змінною середовища PORT (за замовчуванням 5000)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
