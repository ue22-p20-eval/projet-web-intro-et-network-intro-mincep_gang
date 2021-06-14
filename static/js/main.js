

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
            //flèches directionnelles pour J1
            case 37:
                socket.emit("move1", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move1", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move1", {dx:1, dy:0});
                break;
            case 40:
                socket.emit("move1", {dx:0, dy:1});
                break;
            // Q Z D S pour J2
            case 81:
                socket.emit("move2", {dx:-1, dy:0});
                break;
            case 90:
                socket.emit("move2", {dx:0, dy:-1});
                break;
            case 68:
                socket.emit("move2", {dx:1, dy:0});
                break;
            case 83:
                socket.emit("move2", {dx:0, dy:1});
                break;
        }


    };
    
    var btn_n1 = document.getElementById("go_n1");
    btn_n1.onclick = function(e) {
        console.log("Player 1 clicked on button north");
        socket.emit("move1", {dx:0, dy:-1});
    };

    var btn_s1 = document.getElementById("go_s1");
    btn_s1.onclick = function(e) {
        console.log("Player 1 clicked on button south");
        socket.emit("move1", {dx:0, dy:1});
    };

    var btn_w1 = document.getElementById("go_w1");
    btn_w1.onclick = function(e) {
        console.log("Player 1 clicked on button w");
        socket.emit("move1", {dx:-1, dy:0});
    };

    var btn_e1 = document.getElementById("go_e1");
    btn_e1.onclick = function(e) {
        console.log("Player 1 clicked on button e");
        socket.emit("move1", {dx:1, dy:0});
    };

    var btn_n2 = document.getElementById("go_n2");
    btn_n2.onclick = function(e) {
        console.log("Player 2 clicked on button north");
        socket.emit("move2", {dx:0, dy:-1});
    };

    var btn_s2 = document.getElementById("go_s2");
    btn_s2.onclick = function(e) {
        console.log("Player 2 clicked on button south");
        socket.emit("move2", {dx:0, dy:1});
    };

    var btn_w2 = document.getElementById("go_w2");
    btn_w2.onclick = function(e) {
        console.log("Player 2 clicked on button w");
        socket.emit("move2", {dx:-1, dy:0});
    };

    var btn_e2 = document.getElementById("go_e2");
    btn_e2.onclick = function(e) {
        console.log("Player 2 clicked on button e");
        socket.emit("move2", {dx:1, dy:0});
    };

    //actualisation de la position du joeur sur le frontend
    socket.on("response", function(data){    
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
    });
    socket.on("RAS1",function(data){
        var bar = document.getElementById("status_bar_1");
        bar.textContent="Keep looking for bananas";
    });

    socket.on("RAS2",function(data){
        var bar = document.getElementById("status_bar_2");
        bar.textContent="Keep looking for bananas";
    });

    //actualisation des PV de J1 après rencontre avec un monstre
    socket.on("update_health1", function(data) {  
        console.log("A monster!");
        update_health(1, data.health)
        var bar = document.getElementById("status_bar_1");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A ghost? Run! It made you lose  '+data.hp_loss+' health point...');
    });

    //Pareil pour J2
    socket.on("update_health2", function(data) {   
        console.log("A monster!");
        update_health(2, data.health)
        var bar = document.getElementById("status_bar_2");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A ghost? Run! It made you lose  '+data.hp_loss+' health point...');
    });

    // Actualisation des PV de J1 et J2 après rencontre entre eux
    socket.on("update_both_health", function(data){   
        console.log("Internal conflict!");
        update_health(1, data.health1)
        var bar1 = document.getElementById("status_bar_1");
        bar1.textContent="";
        bar1.insertAdjacentHTML('afterbegin','That was a good fight! But you both lose 2 health points...');
        update_health(2, data.health2)
        var bar2 = document.getElementById("status_bar_2");
        bar2.textContent="";
        bar2.insertAdjacentHTML('afterbegin','That was a good fight! But you both lose 2 health points...');

    });

    // Actualisation bananes J1
    socket.on("update_bananas1", function(data) {   
        var bn = document.getElementById("bananas_1");
        bn.innerHTML="Bananas : " + data.bananas + " &#x1F34C;";
        var bar = document.getElementById("status_bar_1");
        bar.textContent="A banana! What a lucky monkey !";
    });

     // Pareil J2
    socket.on("update_bananas2", function(data) {  
        var bn = document.getElementById("bananas_2");
        bn.innerHTML="Bananas : " + data.bananas + " &#x1F34C;";
        var bar = document.getElementById("status_bar_2");
        bar.textContent="A banana! Even frogs like it !";
    });

    // Actualisation PV J1 après coeur
    socket.on("update_health_good1", function(data){  
        console.log("Heart!");
        update_health(1,data.health)
        var bar = document.getElementById("status_bar_1");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A heart! You regained '+data.hp_gain+' health point');
    });

    // Pareil J2
    socket.on("update_health_good2", function(data){   
        console.log("Heart!");
        update_health(2,data.health)
        var bar = document.getElementById("status_bar_2");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A heart! You regained '+data.hp_gain+' health point');


    });

    // Actualisation position des monstres sur frontend
    socket.on("monster_response",function(datas){    
        for(var data of datas){
        console.log(data)
                for( let k=0; k<2; k++){
                    var cell_id = "cell " + data[0][k].i + "-" + data[0][k].j;
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[0][k].content;            
                }
        }
        
    });

    // Requête au serveur de changer de niveau
    socket.on("level_up",function(data){             
        socket.emit("new_game", {level:data.level});

    });

    socket.on("reload_map", function(data){        
        console.log("CHANGE MAP");
        document.location.reload();

        
    });

    // Actualisation de toutes les informations du frontend (s'éxecute périodiquement)
    socket.on("update_all",function(data){     
        console.log("update");
        var bar = document.getElementById("level");
        if (data.level == 1){
            obj=10
        }
        if (data.level == 2){
            obj=40
        }
        if (data.level==3){
            obj= 100
        }
        bar.textContent=" Level " +data.level+ ' : Collect a total of '+obj+' bananas';
        var bn1 = document.getElementById("bananas_1");
        bn1.innerHTML="Bananas : " + data.bananas1 + " &#x1F34C;";
        var bn2 = document.getElementById("bananas_2");
        bn2.innerHTML="Bananas : " + data.bananas2 + " &#x1F34C;";
        update_health(1,data.health1)
        update_health(2,data.health2)
    });

     //Message de fin
    socket.on("game_over_1",function(data){ 
        console.log("Game over player 1");
        death="Player 1";
        if (data.health2==0){  // Au cas où J2 aurait aussi perdu en même temps (ex: rencontre entre joueurs)
            death="Both players";
        }
        var end=document.getElementById("game_over"); //Effacement de toute l'interface frontend
        end.textContent="";
        end.insertAdjacentHTML('afterbegin','<h2><div class="game_over_screen"><h1> <div class= "end_message">Game over <br><br>' + death + ' died</div></h1><h3> <div class= "player_1_results"> <h2><div id= "player_1_profile"> Player 1 &#128053 :</div></h2><div id= "player_1_health"> Remaining health : ' + data.health1 + '</div><div id= "player_1_bananas">Bananas : ' + data.bananas1 + '</div></div><div class= "player_2_results"><h2><div id= "player_2_profile"> Player 2 &#128056 :</div></h2><div id= "player_2_health"> Remaining health : ' + data.health2 + '</div> <div id= "player_2_bananas">Bananas : ' + data.bananas2 + '</div></div> </h3> </div></h2>');
        //On réécrit le HTML pour afficher les scores finaux
    });

    //Pareil pour J2
    socket.on("game_over_2",function(data){ 
        console.log("Game over player 2");
        death="Player 2";
        if (data.health1==0){
            death="Both players"
        }
        var end=document.getElementById("game_over");
        end.textContent="";
        end.insertAdjacentHTML('afterbegin','<h2><div class="game_over_screen"><h1> <div class= "end_message">Game over <br><br>' + death +' died</div></h1><h3> <div class= "player_1_results"> <h2><div id= "player_1_profile"> Player 1 &#128053 :</div></h2><div id= "player_1_health"> Remaining health : ' + data.health1 + '</div><div id= "player_1_bananas">Bananas : ' + data.bananas1 + '</div></div><div class= "player_2_results"><h2><div id= "player_2_profile"> Player 2 &#128056 :</div></h2><div id= "player_2_health"> Remaining health : ' + data.health2 + '</div> <div id= "player_2_bananas">Bananas : ' + data.bananas2 + '</div></div> </h3> </div></h2>');
    });

    //Message victoire (niveau 3 complété)
    socket.on("win",function(data){  
        console.log("Victory!");
        winner="Both players";
        if (data.bananas1>data.bananas2){
            winner="Player 1"
        }
        if (data.bananas2>data.bananas1){
            winner="Player 2"
        }
        var end=document.getElementById("game_over"); //On efface tout puis on réécrit
        end.textContent="";
        end.insertAdjacentHTML('afterbegin','<h2><div class="game_over_screen"><h1> <div class= "end_message">Well played! <br><br>' + winner +' won !</div></h1><h3> <div class= "player_1_results"> <h2><div id= "player_1_profile"> Player 1 &#128053 :</div></h2><div id= "player_1_health"> Remaining health : ' + data.health1 + '</div><div id= "player_1_bananas">Bananas : ' + data.bananas1 + '</div></div><div class= "player_2_results"><h2><div id= "player_2_profile"> Player 2 &#128056 :</div></h2><div id= "player_2_health"> Remaining health : ' + data.health2 + '</div> <div id= "player_2_bananas">Bananas : ' + data.bananas2 + '</div></div> </h3> </div></h2>');
    });

    //Actualise les PV sur le frontend
    function update_health(player_id, health){ 
        var id_HTML = "health_points_" + String(player_id);
        var hp = document.getElementById(id_HTML);
        var hp_car = "Health : ";
        for (var j=0; j<health; j++){
            hp_car = hp_car + "&#128150;";
        }
        hp.innerHTML = hp_car;
    };

});