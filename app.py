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

    @socketio.on("move1")
    def on_move_msg(json, methods=["GET", "POST"]):
        print("player 1 moves")
        dx = json['dx']
        dy = json["dy"]
        data, ret,hp_loss, hp_gain, banana_gain, conflict= game.move_1(dx,dy)
        player_health=game._player1.health_points
        if conflict==True:
            game._player1.health_points=max(0,game._player1.health_points-30)
            game._player2.health_points=max(0,game._player2.health_points-30)
            for i in range(4):
                datas=game.players_shock(game._player1,dx,dy)
                socketio.emit("update_bananas1", {"bananas" : game._player1.bananas})
                socketio.emit("update_health1", {"health" : game._player1.health_points,"hp_loss":f'{0}'})
                socketio.emit("update_bananas2", {"bananas" : game._player2.bananas})
                socketio.emit("update_health2", {"health" : game._player2.health_points,"hp_loss":f'{0}'})
                socketio.emit("response",datas[1])
                socketio.emit("response",datas[0])
            socketio.emit("update_both_health",{"health1":game._player1.health_points,"health2":game._player2.health_points})
        if player_health==0:
            socketio.emit("game_over_1",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":0,"health2":game._player2.health_points})
        if ret:
            print("joueur 1",data)
            socketio.emit("response", data)
            if hp_loss !=0:
                socketio.emit("update_health1", {"health" : player_health,"hp_loss":f'{hp_loss}'})
            elif banana_gain !=0:
                socketio.emit("update_bananas1", {"bananas" : game._player1.bananas})
            elif hp_gain!=0:
                socketio.emit("update_health_good1", {"health" : player_health,"hp_gain":f'{hp_gain}'})


            else:
                socketio.emit("RAS1",data)
        print("health1", player_health)
    
    @socketio.on("move2")
    def on_move_msg(json, methods=["GET", "POST"]):
        print("player 2 moves")
        dx = json['dx']
        dy = json["dy"]
        data, ret,hp_loss, hp_gain, banana_gain,conflict= game.move_2(dx,dy)
        player_health = game._player2.health_points
        if conflict==True:
            game._player1.health_points=max(0,game._player1.health_points-30)
            game._player2.health_points=max(0,game._player2.health_points-30)
            for i in range(4):
                datas=game.players_shock(game._player2,dx,dy)
                socketio.emit("update_bananas1", {"bananas" : game._player1.bananas})
                socketio.emit("update_health1", {"health" : game._player1.health_points,"hp_loss":f'{0}'})
                socketio.emit("update_bananas2", {"bananas" : game._player2.bananas})
                socketio.emit("update_health2", {"health" : game._player2.health_points,"hp_loss":f'{0}'})
                socketio.emit("response",datas[0])
                socketio.emit("response",datas[1])
            socketio.emit("update_both_health",{"health1":game._player1.health_points,"health2":game._player2.health_points})
        if player_health==0:
            socketio.emit("game_over_2",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":0})
        if ret:
            print("joueur 2",data)
            socketio.emit("response", data)
            if hp_loss !=0:
                socketio.emit("update_health2", {"health" : player_health,"hp_loss":f'{hp_loss}'})
            elif banana_gain!=0:
                socketio.emit("update_bananas2", {"bananas" : game._player2.bananas})
            elif hp_gain!=0:
                socketio.emit("update_health_good2", {"health" : player_health,"hp_gain":f'{hp_gain}'})


            else:
                socketio.emit("RAS2",data)
        print("health2", player_health)


def periodic_event():    
    while True:  
        print("ok")
        data_monstres=game.update_monster()
        socketio.emit("monster_response", data_monstres)
        if game._player1.health_points==0:
            socketio.emit("game_over_1",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":0})
        if game._player2.health_points==0:
            socketio.emit("game_over_2",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":0})
        time.sleep(1.5)


threading.Thread(target=request_waiter).start()
threading.Thread(target=periodic_event).start()

if __name__=="__main__":
    socketio.run(app, port=5001)