

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
            case 37:
                socket.emit("move", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0});
                break;
            case 40:
                socket.emit("move", {dx:0, dy:1});
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});
    };


    socket.on("response", function(data){
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
    });
    socket.on("RAS",function(data){
        var bar = document.getElementById("status_bar");
        bar.textContent="Keep going";
    });

    socket.on("update_health", function(data) {
        console.log("A monster!");
        player_health = data.health;
        var hp = document.getElementById("health_points");
        hp.innerHTML="Health : " + player_health +"/100";
        var bar = document.getElementById("status_bar");
        bar.textContent="You killed the monster, but you lost "+data.hp_loss+" health points..";
    });

    socket.on("invalid_movement",function(data){
        console.log("Invalid movement");
        var bar = document.getElementById("status_bar");
        bar.textContent="There is a wall";
    });
    socket.on("monster_response",function(datas){
        data=datas[0]
                for( var k=0; i<2; i++){
                    var cell_id = "cell " + data[k].i + "-" + data[k].j;
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[k].content;            
                }
            
        
        
    });


});