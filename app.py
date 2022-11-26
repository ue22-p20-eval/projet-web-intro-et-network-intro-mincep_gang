import game_backend
from game_backend.monsters import Monsters
from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game
from game_backend import Generator
import time
import threading
import random


app = Flask(__name__)
socketio = SocketIO(app)

levels=[[10,15,20],[20,50,10],[30,80,3]]   # Les 3 niveaux sont representés par respectivement leur nombre de monstres, bananes et coeurs.
nb_monsters, nb_bananas, nb_hearts= levels[0]
game = Game(number_monsters=nb_monsters,number_bananas=nb_bananas,number_hearts=nb_hearts) #On lance le jeu avec les valeurs du 1er niveau



def request_waiter():

    @app.route("/")
    def index():
        map = game.getMap()       #initialise la carte
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

    @socketio.on("move1")  #ce que fait le J1 quand il bouge
    def on_move_msg(json, methods=["GET", "POST"]):
        print("player 1 moves")
        dx = json['dx']
        dy = json["dy"]
        data, ret,hp_loss, hp_gain, banana_gain, conflict= game.move_1(dx,dy)   # mouvement de J1, on récupère aussi des infos: perte/gain de PV, rencontre avec l'autre joueur
        player_health=game._player1.health_points
        if conflict==True:       #en cas de rencontre avec l'autre joueur
            game._player1.health_points=max(0,game._player1.health_points-2)
            game._player2.health_points=max(0,game._player2.health_points-2)
            for i in range(4): # les deux joueurs vont automatiquement reculer de 4 cases chacun, et mettre à jour leur score/ PV en fonctions des éléments qu'ils auront rencontré
                datas=game.players_shock(game._player1,dx,dy)  #fait automatiquement bouger les joueurs d'une case dans des directions opposés
                socketio.emit("update_bananas1", {"bananas" : game._player1.bananas})    #MAJ bananes J1
                socketio.emit("update_health1", {"health" : game._player1.health_points,"hp_loss":f'{0}'})  #MAJ PV J1 
                socketio.emit("update_bananas2", {"bananas" : game._player2.bananas})    #MAJ bananes J2
                socketio.emit("update_health2", {"health" : game._player2.health_points,"hp_loss":f'{0}'})  #MAJ PV J2
                socketio.emit("response",datas[1])  #actualisation de la position de J2 sur le frontend
                socketio.emit("response",datas[0])  # '''''''''''''''''''''''''''''' J1  '''''''''''''
            socketio.emit("update_both_health",{"health1":game._player1.health_points,"health2":game._player2.health_points}) #MAJ PV J1 et J2
        if player_health==0: #après les changements de vie on teste les conditions de game over
            socketio.emit("game_over_1",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":0,"health2":game._player2.health_points})
        if ret:  #si J1 a le droit de bouger (partout sauf dans mur ou dans J2)
            socketio.emit("response", data)
            if hp_loss !=0:  #si perte de PV, on actualise sur le frontend
                socketio.emit("update_health1", {"health" : player_health,"hp_loss":f'{hp_loss}'})
            elif banana_gain !=0: #pareil pour les bananes
                socketio.emit("update_bananas1", {"bananas" : game._player1.bananas})
            elif hp_gain!=0:   #pareil pour les coeurs
                socketio.emit("update_health_good1", {"health" : player_health,"hp_gain":f'{hp_gain}'})


            else:  #si déplacement sur le sol
                socketio.emit("RAS1",data)
    
    @socketio.on("move2")  #même fonction, du côté de J2
    def on_move_msg(json, methods=["GET", "POST"]):

        print("player 2 moves")
        dx = json['dx']
        dy = json["dy"]
        data, ret,hp_loss, hp_gain, banana_gain,conflict= game.move_2(dx,dy)
        player_health = game._player2.health_points
        if conflict==True:
            game._player1.health_points=max(0,game._player1.health_points-2)
            game._player2.health_points=max(0,game._player2.health_points-2)
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
            socketio.emit("response", data)
            if hp_loss !=0:
                socketio.emit("update_health2", {"health" : player_health,"hp_loss":f'{hp_loss}'})
            elif banana_gain!=0:
                socketio.emit("update_bananas2", {"bananas" : game._player2.bananas})
            elif hp_gain!=0:
                socketio.emit("update_health_good2", {"health" : player_health,"hp_gain":f'{hp_gain}'})


            else:
                socketio.emit("RAS2",data)

    @socketio.on("new_game")  #si on augmente de nouveau, il faut réinitialiser la carte et les positions de J1, J2, monstres et items
    def on_move_msg(json, methods=["GET", "POST"]):

        nb_monsters, nb_bananas,  nb_hearts= levels[json['level']-1]  #nouvelles valeurs
        game._generator = Generator(width=50, height=28)
        game._generator.gen_level()
        game._generator.gen_tiles_level()
        game._map = game._generator.tiles_level
        game._player1.initPos( game._map )  #réinitialisation des positions sans créer de nouveau joueurs (conservation des PV/ du score)
        game._player2.initPos( game._map )
        game._Monsters = game._generator.gen_monster(nb_monsters,game)
        game._Items= game._generator.gen_item(nb_bananas,nb_hearts,game)
        socketio.emit("reload_map",{"level":json['level'],"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":game._player2.health_points})
        #on recherche la page pour que la carte s'affiche

def periodic_event():    #toutes les secondes, mouvement des monstres, MAJ des PV/du score de chacun, test de la condition  game over 
    level=1
    limit_bananas=10  #objectif de bananes pour le niveau 1
    while True:    
        print("tic tac")
        socketio.emit("update_all",{"level":level,"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":game._player2.health_points})
        data_monstres=game.update_monster()  #mouvement de chaque monstre
        for data in data_monstres:
            if data[1]==1: #le monstre a touché J1
                game._player1.health_points=max(0,game._player1.health_points-1)
                socketio.emit("update_health1", {"health" :game._player1.health_points ,"hp_loss":1})
            if data[1]==2: #le monstre a touché J2
                game._player2.health_points=max(0,game._player2.health_points-1)
                socketio.emit("update_health2", {"health" :game._player2.health_points ,"hp_loss":1})
        socketio.emit("monster_response", data_monstres)  #actualisation position des monstres sur frontend
        if game._player1.health_points==0: 
            socketio.emit("game_over_1",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":game._player2.health_points})
        if game._player2.health_points==0:
            socketio.emit("game_over_2",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":game._player2.health_points})
        if game._player1.bananas+game._player2.bananas==limit_bananas:  #condition validation de l'objectif du niveau
            level+=1
            if level==4: #le jeu est alors fini (que 3 niveaux)
                socketio.emit("win",{"bananas1": game._player1.bananas, "bananas2": game._player2.bananas,"health1":game._player1.health_points,"health2":game._player2.health_points})
            else:
                print("level up!")
                socketio.emit("level_up",{"level":level}) #actualisation du frontend, + requête de changement de niveau 
                limit_bananas+=levels[level-1][1]-20  #nouvel objectif de bananes
            
        time.sleep(1)  #boucle infinie qui se répète chaque seconde


threading.Thread(target=request_waiter).start()  #2 threads pour gérer la boucle infinie
threading.Thread(target=periodic_event).start()

if __name__=="__main__":
    socketio.run(app, port=5001)