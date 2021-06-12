from game_backend.monsters import Monsters
from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game
import time
import threading
import random


app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


def request_waiter():

    @app.route("/")
    def index():
        map = game.getMap()
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

    @socketio.on("move")
    def on_move_msg(json, methods=["GET", "POST"]):
        print("received move ws message")
        dx = json['dx']
        dy = json["dy"]
        data, ret,hp_loss= game.move(dx,dy)
        player_health = game.get_player_health()
        player_health = max(0,player_health - hp_loss)
        if player_health==0:
            socketio.emit("game_over",{"Message": "Well played"})
        if ret:
            print("joueur",data)
            socketio.emit("response", data)
            if hp_loss !=0:
                socketio.emit("update_health", {"health" : player_health,"hp_loss":f'{hp_loss}'})
            else:
                socketio.emit("RAS",data)
        else:
            socketio.emit("invalid_movement", data)
        print("health", player_health)

def monster_move():    
    while True: 
        hp_loss=0 
        print("ok")
        data_monstres=game.update_monster()
        socketio.emit("monster_response", data_monstres)
        time.sleep(0.5)


threading.Thread(target=request_waiter).start()
threading.Thread(target=monster_move).start()

"""
@socketio.on("update_monster")
def monster_move():
    
    if time > 0.02:
        move_time = time()
        print("monster moved")
        #pour faire bouger le monstre
        data_monstre, ret = game.update_Monster()
        socketio.emit("monster_response", data_monstre)
        time = 0

"""

if __name__=="__main__":
    socketio.run(app, port=5001)