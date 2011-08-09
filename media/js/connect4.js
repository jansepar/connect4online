//global variables
var board_color = "yellow";
var board_width = 525;
var board_height = 450;
var canvas_width = 525;
var canvas_height = 525;
var cell_size = 75;
var puckRadius = 35;
var num_rows = 6;
var num_cols = 7;
var held_y = 35;
var held_x;
var puck_cells; //2D array
var num_dropped; // array
var intervalId;

var cell_colors = ["WHITE", "RED", "BLACK"]

var TURN; // Player 1 or 2
var PLAYER;
var GAME_STATE; // STARTING, WAITING, RUNNING
var GAME_ID;

var context;

function onMouseMove(evt) {

	if (evt.pageX > canvasMinX && evt.pageX < canvasMaxX) {
		held_x = evt.pageX - canvasMinX - (puckRadius/2);
	}

}

function circle(x, y, r, color) {
	context.beginPath();
	context.arc(x, y, r, 0, Math.PI*2, true);
	context.fillStyle = color;
	context.closePath();
	context.fill();
}

function drawGameBoard() {
	// draw the yellow background
	context.beginPath();
	context.rect(0, canvas_height - board_height, board_width, board_height);
	context.fillStyle = board_color;
	context.closePath();
	context.fill();

	// draw alignment grid for guiding players
	for (var x = 0; x <= board_width; x += cell_size) {
		context.moveTo(x, canvas_height - board_height);
		context.lineTo(x, canvas_height);
	}
		
	for (var y = canvas_height - board_height; y <= board_height; y += cell_size) {
		context.moveTo(0, y);
		context.lineTo(canvas_width, y);
	}

	context.stroke();

	start_x = cell_size + cell_size/2;
	// fill in cells for the grid
	for (var x = 0; x < num_rows; x++) {
		for (var y = 0; y < num_cols; y++) {
			context.beginPath();
			context.arc(y*cell_size + cell_size/2, (x+1)*cell_size + cell_size/2, puckRadius, 0, Math.PI*2, true);
			context.fillStyle = cell_colors[puck_cells[x][y].player];
			context.closePath();
			context.fill();
			
		}
	}

	
}

function drawHeld() {

	circle(held_x, held_y, puckRadius, cell_colors[TURN]);

}

function clear() {
	// clear the canvas
	context.clearRect(0, 0, canvas_width, canvas_height);
}


function checkWin(row, col){


	// check for win on row
	var connect4 = 0;
	for(var i=0; i< num_cols; i++) {
		if (puck_cells[row][i].player == TURN) {
			connect4++;
			if (connect4 == 4){
				return true; //TODO: potentially return coordinates
			}
		}
		else {
			connect4 = 0;
		}
	}
	connect4 = 0;

	// check for win on column
	for(var i=0; i< num_rows; i++) {
		if (puck_cells[i][col].player == TURN) {
			connect4++;
			if (connect4 == 4){
				return true; //TODO: potentially return coordinates
			}
		}
		else {
			connect4 = 0;
		}
	}
	connect4 = 0;

	// check for win on left diagonal

	// find coordinates of top left coordinate of left diagonal
	var itr_row, itr_col;

	if(row >= col){
		itr_col = 0;
		itr_row = row - col;
	}
	else{
		itr_col = col - row;	
		itr_row = 0;
	}

	// iterate from top left coordinate and check for 4 in a row
	while(itr_row < num_rows && itr_col < num_cols){
		
		console.log("Leftd: Row: " + itr_row + " " + "Col: " + itr_col);
		if (puck_cells[itr_row][itr_col].player == TURN) {
			connect4++;
			if (connect4 == 4){
				return true; //TODO: potentially return coordinates
			}
		}
		else {
			connect4 = 0;
		}
		itr_row++;
		itr_col++;
		
	}

	// check for win on the right diagonal

	// find coordinates of top left coordinate of left diagonal
	var itr_row, itr_col;

	if(row <= num_cols - col - 1){
		itr_row = 0;
		itr_col = col + row;
	}
	else{
		itr_col = num_cols - 1;	
		itr_row = row - (num_cols - col - 1);
	}

	// iterate from top left coordinate and check for 4 in a row
	while(itr_row < num_rows && itr_col >= 0){
		
		console.log("Rightd: Row: " + itr_row + " " + "Col: " + itr_col);
		if (puck_cells[itr_row][itr_col].player == TURN) {
			connect4++;
			if (connect4 == 4){
				return true; //TODO: potentially return coordinates
			}
		}
		else {
			connect4 = 0;
		}
		itr_row++;
		itr_col--;
		
	}


	return false;
}

function setBoardData(drop_column, playerId) {
// sets the data for the column

		drop_row = num_rows - num_dropped[drop_column] - 1

		// modify global variables
		puck_cells[drop_row][drop_column].player = playerId;
		num_dropped[drop_column] += 1;

}

function dropPuck() {

	if (GAME_STATE == "RUNNING"){

		GAME_STATE = "WAITING";

		// determine the column to drop the puck
		drop_column = Math.ceil(held_x/cell_size) - 1;
		setBoardData(drop_column, PLAYER);

		// check to see if there is a winner
		win_check = checkWin(drop_row, drop_column);

		if (win_check == true){
			// TODO: execute some ajax call to register the win
			document.getElementById("status").innerHTML = "Player " + TURN + " wins!";
			GAME_STATE = "FINISHED";
			document.getElementById("error").innerHTML = "Player " + TURN + " wins!";
			
		}
		send_move(drop_column);

			// Switch turns 
			/* Not needed for multiplayer
			if (TURN == 1) {
				TURN = 2;
			}else {
				TURN = 1;
			}
			*/



	}

}

function initCells() {
	// Initiate puck cells
	puck_cells = new Array(num_rows);
	for (var i=0; i < num_rows; i++) {
		puck_cells[i] = new Array(num_cols);
		for (var j=0; j < num_cols; j++) {
			puck_cells[i][j] = new Puck(0);
		}
	}

	num_dropped = new Array(num_cols);
	for (var i=0; i < num_cols; i++) {
		num_dropped[i] = 0;
	}
}

function Puck(player) {
// function object for a puck
	this.player = player; // 0 = none, 1 = p1, 2 = p2
}

function init_game() {
// creates request to initialize game
	$.ajax(
	{
		type: 'GET',
		url: "/initialize_game/",
		dataType: 'json',
		success: function(data) {
			document.getElementById("status").innerHTML = "Waiting for other players...";
			document.getElementById("info").innerHTML = "Game id: " + data.game_id;
			GAME_ID = data.game_id;
			TURN = data.player;
			GAME_STATE = "WAITING";
			if (data.gameStatus === "open") {
				get_challenger();
			} else if (data.gameStatus === "closed"){
				document.getElementById("status").innerHTML = "Challenger " + data.opponent + " found!";
				get_turn();
			}
			PLAYER = data.player;
		}, 
		
	});

}

function get_challenger() {
// checks if the gamesession has another player to play with yet

	var intervalId = setInterval(function()
	{
		$.ajax(
		{
			url: "/get_challenger/",
			data: {gameid: GAME_ID},
			dataType: 'json',
			success: function(data) {
				if (data.gameStatus === "COMPLETE") {
					GAME_STATE = "RUNNING";
					document.getElementById("status").innerHTML = "Challenger " + data.opponent + " found!";
					clearInterval(intervalId);
				}

			},

		})

	}, 1000);

}

function get_turn() {
// polls to check if it is the players turn to go 

	var intervalid = setInterval(function()
	{
		$.ajax(
		{
			url: "/get_turn/",
			data: {gameid: GAME_ID},
			dataType: 'json',
			success: function(data) {
				console.log(data.turn);
				if (data.turn === PLAYER) {
					var opponent;
					if (PLAYER === 1){
						opponent = 2;
					}else{
						opponent = 1;
					}
					setBoardData(data.previous, opponent); 
					GAME_STATE = "RUNNING";
					document.getElementById("status").innerHTML = "Make a move";
					clearInterval(intervalid);
					// TODO: Get previous col	
				}

			},

		})

	}, 1000);

}

function send_move(column) {



	GAME_STATE = "WAITING";
	document.getElementById("status").innerHTML = "Make a move";

	$.ajax(
	{
		type: 'GET',
		url: "/send_move/",
		data: {"column": column, "gameid": GAME_ID},
		dataType: 'json',
		success: function(data) {
			if(data.success === true) {
				document.getElementById("status").innerHTML = "Action sent. Waiting for turn...";
				document.getElementById("error").innerHTML = "";
				//clearInterval(intervalId);
				get_turn();
			}
			else {
				// Must still check for valid column sent incase of hacking
				document.getElementById("error").innerHTML = "The move you made was invalid";
				send_move(column);
				GAME_STATE = "RUNNING"
			}
		}, 
		
	});


}

function init() {

	// set game state to waiting
	GAME_STATE = "STARTING";


	// set status div to inform user of game state
	document.getElementById("status").innerHTML = "Creating game...";

	//get a reference to the context
	canvas = document.getElementById("canvas")
	context = canvas.getContext("2d");

	// initial position of held puck
	held_x = 35;

	// set stroke style for boundary lines in game board
	context.strokeStyle = "#eee";

	// set bounds for canvas
	canvasMinX = $("#canvas").offset().left;
	canvasMaxX = canvasMinX + canvas_width;

	// set the documents mouse move handler to onMouseMove
	$(document).mousemove(onMouseMove);

	// set the onclick handler of the canvas to our mouse click handler function
	canvas.onclick = dropPuck;

	init_game();

	var draw = function() {  // experimenting with closures TODO fix up for better use of them
		// clears the canvas on each loop
		clear();

		// draw the held puck if the game has started
		if (GAME_STATE != "STARTING") {
			drawHeld();
		}

		// draw the game board
		drawGameBoard();
	}

	intervalId = setInterval(draw, 34); //draw at ~30fps instead of every 10 ms, big performance boost

	return intervalId;

}

window.onload = function(){
	initCells();
	init();
};
