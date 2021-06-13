

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
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
            case 65:
                socket.emit("move2", {dx:-1, dy:0});
                break;
            case 87:
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

    socket.on("update_health1", function(data) {
        console.log("A monster!");
        player_health = data.health;
        var hp = document.getElementById("health_points_1");
        hp.innerHTML="Health : " + player_health +"/100";
        var bar = document.getElementById("status_bar_1");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A ghost? Run! It made you lose  '+data.hp_loss+' health points..');
    });

    socket.on("update_health2", function(data) {
        console.log("A monster!");
        player_health = data.health;
        var hp = document.getElementById("health_points_2");
        hp.innerHTML="Health : " + player_health +"/100";
        var bar = document.getElementById("status_bar_2");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A ghost? Run! It made you lose  '+data.hp_loss+' health points..');
    });

    socket.on("update_both_health", function(data){
        console.log("Internal conflict!");
        var hp1 = document.getElementById("health_points_1");
        hp1.innerHTML="Health : " + data.health1 +"/100";
        var bar1 = document.getElementById("status_bar_1");
        bar1.textContent="";
        bar1.insertAdjacentHTML('afterbegin','That was a good fight! But you both lose 30 health points..');
        var hp2 = document.getElementById("health_points_2");
        hp2.innerHTML="Health : " + data.health2 +"/100";
        var bar2 = document.getElementById("status_bar_2");
        bar2.textContent="";
        bar2.insertAdjacentHTML('afterbegin','That was a good fight! But you both lose 30 health points..');

    });

    socket.on("update_bananas1", function(data) {
        var hp = document.getElementById("bananas_1");
        hp.innerHTML="Bananas : " + data.bananas;
        var bar = document.getElementById("status_bar_1");
        bar.textContent="A banana! What a lucky monkey !";
    });


    socket.on("update_bananas2", function(data) {
        var hp = document.getElementById("bananas_2");
        hp.innerHTML="Bananas : " + data.bananas;
        var bar = document.getElementById("status_bar_2");
        bar.textContent="A banana! Even frogs like it !";
    });

    socket.on("update_health_good1", function(data){
        console.log("Heart!");
        player_health=data.health
        var hp = document.getElementById("health_points_1");
        hp.innerHTML="Health : " + player_health +"/100";
        var bar = document.getElementById("status_bar_1");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A heart! You regained '+data.hp_gain+' health points');
    });

    socket.on("update_health_good2", function(data){
        console.log("Heart!");
        player_health=data.health
        var hp = document.getElementById("health_points_2");
        hp.innerHTML="Health : " + player_health +"/100";
        var bar = document.getElementById("status_bar_2");
        bar.textContent="";
        bar.insertAdjacentHTML('afterbegin','A heart! You regained '+data.hp_gain+' health points');


    });

    socket.on("monster_response",function(datas){
        for(var data of datas){
        console.log(data)
                for( let k=0; k<2; k++){
                    var cell_id = "cell " + data[k].i + "-" + data[k].j;
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[k].content;            
                }
        }
        
    });

    socket.on("game_over_1",function(data){
        console.log("Game over player 1");
        death="Player 1";
        if (data.health2==0){
            death="Both players";
        }
        var end=document.getElementById("game_over");
        end.textContent="";
        end.insertAdjacentHTML('afterbegin','<h2><div class="game_over_screen"><h1> <div class= "end_message">Game over <br><br>' + death + ' died !</div></h1><h3> <div class= "player_1_results"> <h2><div id= "player_1_profile"> Player 1:</div></h2><div id= "player_1_health"> Remaining health : ' + data.health1 + '</div><div id= "player_1_bananas">Bananas : ' + data.bananas1 + '</div></div><div id= "player_2_results"><h2><div id= "player_2_profile"> Player 2:</div></h2><div id= "player_2_health"> Remaining health : ' + data.health2 + '</div> <div id= "player_2_bananas">Bananas : ' + data.bananas2 + '</div></div> </h3> </div></h2>');
    });

    socket.on("game_over_2",function(data){
        console.log("Game over player 2");
        death="Player 2";
        if (data.health1==0){
            death="Both players"
        }
        var end=document.getElementById("game_over");
        end.textContent="";
        end.insertAdjacentHTML('afterbegin','<h2><div class="game_over_screen"><h1> <div class= "end_message">Game over <br><br>' + death +' died !</div></h1><h3> <div class= "player_1_results"> <h2><div id= "player_1_profile"> Player 1:</div></h2><div id= "player_1_health"> Remaining health : ' + data.health1 + '</div><div id= "player_1_bananas">Bananas : ' + data.bananas1 + '</div></div><div id= "player_2_results"><h2><div id= "player_2_profile"> Player 2:</div></h2><div id= "player_2_health"> Remaining health : ' + data.health2 + '</div> <div id= "player_2_bananas">Bananas : ' + data.bananas2 + '</div></div> </h3> </div></h2>');
    });
});