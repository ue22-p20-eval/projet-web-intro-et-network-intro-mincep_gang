from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game
from time import time



app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


time = time()


@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]
    
    data, ret = game.move(dx,dy)
    if ret:
        socketio.emit("response", data)

                
@socketio.on("update_monster")
def monster_move():
    
    if time > 0.02:
        move_time = time()
        print("monster moved")
        #pour faire bouger le monstre
        data_monstre, ret = game.update_Monster()
        socketio.emit("monster_response", data_monstre)
        time = 0


if __name__=="__main__":
    socketio.run(app, port=5001)


