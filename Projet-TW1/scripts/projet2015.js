/***********************************************/
/**                                            */
/**              MINI-PROJET JS 2015           */
/**         TEXIER Léane et AUVRAY Claire      */
/***********************************************/


//Definitions de variables

var myCanvas ;
var context;
var vaisseau;
var x_vaisseau;
var y_vaisseau;
var tirImg;
var allTir = new Array();
var soucoupeSize ;
var soucoupeImg;
var allSoucoupes = new Array();
var affiche_score=0;
var ctrltemp;
var compteur=0;


var setup = function() {
	myCanvas = document.getElementById("stars");
	context = myCanvas.getContext("2d");
	
	vaisseau = new Image();
	vaisseau.src = "images/vaisseau-ballon-petit.png";
	
	tirImg = new Image();
	tirImg.src = "images/tir.png";
	
	vaisseau.addEventListener("load",initial_vaisseau) ;
	window.addEventListener("keydown",keyAction);
	
	window.requestAnimationFrame(moveAndDrawTir);
	
	soucoupeImg = new Image();
	soucoupeImg.src="images/flyingSaucer-petit.png"; 
	
	document.getElementById("nouvelleSoucoupe").addEventListener("click",addSoucoupe);
	soucoupeSize = soucoupeImg.width;
	
    window.requestAnimationFrame(moveAndDrawSoucoupes);
	
	score = document.getElementById('score');
	infini=document.getElementById("flotteSoucoupes");
	infini.addEventListener("click",addSoucoupe2);	
}


/* on charge la fonction setup */
window.addEventListener("load",setup); 

var dessine = function(){
	//Dessine la position du vaisseau
    context.drawImage(vaisseau,x_vaisseau,y_vaisseau);
}

var initial_vaisseau=function(){
	//Position du vaisseau au début du jeu
    x_vaisseau= 40 ;
    y_vaisseau = (myCanvas.height/2)-vaisseau.height/2;
}

var keyAction = function(event) {
	//Gestion des touches. Haut et Bas : le vaisseau bouge. Touche espace : actionne un tir
    switch (event.key) {
        case "ArrowUp":
		case "Up":
			y_vaisseau = Math.max(1,  y_vaisseau-8);   
            break;
        case "ArrowDown": 
		case "Down":
			y_vaisseau= Math.min(myCanvas.height-vaisseau.height, y_vaisseau+8)  ;
            break; 
		case " ":
			addTir(); 
            break;
        default: return;
    }
    event.preventDefault();
}

var tir = function(x_tir,y_tir){
	//Prend les coordonnées d'un tir
	this.x_tir = x_tir;
	this.y_tir = y_tir;
}

var addTir = function(){
	//Ajoute un nouveau tir au tableau des tirs
	var nouveau_tir = new tir (x_vaisseau+vaisseau.width,y_vaisseau+vaisseau.height/2);
	allTir.push(nouveau_tir);
	moveAndDrawTir();
}

var drawTir=function(tir){
	//Dessine les tirs
	for(var j = 0; j < allTir.length; j++) {
		context.drawImage(tirImg , tir.x_tir , tir.y_tir);
		if (tirReussi(tir)){
			allSoucoupes.splice(allSoucoupes.indexOf(tirReussi(tir)),1); /*on supprime la soucoupe */
			j=j-1;
			allTir.splice(j,1); /*on supprime le tir */
			affiche_score=affiche_score+200;
			score.textContent = affiche_score;
		}	
	    if (tir>(myCanvas.width)){ /* Si le tir sort du canvas */
			allTir.splice(j,1);
			}   
	}
}

var moveTir=function(tir){
	//Mouvement des tirs
	context.clearRect(tir.x_tir,tir.y_tir,tirImg.width, tirImg.height);
	tir.x_tir += 8;
}

var moveAndDrawTir = function() { 
	//Dessine et fait bouger les tirs du tableau
    for(var i = 0; i < allTir.length; i++) {		
        moveTir(allTir[i]);
        drawTir(allTir[i]);      
    }
   window.requestAnimationFrame(moveAndDrawTir);
}

var Soucoupe = function(x_soucoupe,y_soucoupe,Delta_x_soucoupe,Delta_y_soucoupe) {
	//Prend les coordonnées d'une soucoupe
    this.xs = x_soucoupe;
    this.ys = y_soucoupe;
    this.deltaX = Delta_x_soucoupe;
    this.deltaY = Delta_y_soucoupe;
}

var alea  = function(max) {
	//Renvoie un nombre aléatoire entre 0 et max
    return Math.floor(Math.random()*max);
} 

var addSoucoupe = function() {  
	// Ajoute une soucoupe ou tableau allSoucoupes
    var xs = myCanvas.width-soucoupeSize;
    var ys = alea(myCanvas.height-soucoupeSize);
    var deltaX = alea(10)-5;
    if (deltaX>=0) deltaX = deltaX+1;
    var deltaY = alea(10)-5;
    if (deltaY>=0) deltaY = deltaY+1;
    allSoucoupes.push(new Soucoupe(xs,ys,deltaX,deltaY));
	this.blur();
}

var drawSoucoupe = function(soucoupe) {
	//Dessine une soucoupe
    context.drawImage(soucoupeImg,soucoupe.xs,soucoupe.ys);
}

var moveSoucoupe = function(soucoupe) {
	//Gère le mouvement des soucoupes
    if (( soucoupe.xs < 0 ) || ( soucoupe.xs > (myCanvas.width) - soucoupeSize )) { soucoupe.deltaX = - soucoupe.deltaX; }
    if (( soucoupe.ys < 0 ) || ( soucoupe.ys > (myCanvas.height) - soucoupeSize)) { soucoupe.deltaY = - soucoupe.deltaY; }
    soucoupe.xs = soucoupe.xs + soucoupe.deltaX;
    soucoupe.ys = soucoupe.ys + soucoupe.deltaY;
}

var moveAndDrawSoucoupes = function() {  
	//Gere le mouvement et dessine les soucoupes
    context.clearRect(0,0,myCanvas.width, myCanvas.height); 
	dessine();
    for(var i = 0; i < allSoucoupes.length; i++) {
        moveSoucoupe(allSoucoupes[i]);
        drawSoucoupe(allSoucoupes[i]);        
        if (collision_soucoupe_sort(allSoucoupes[i])) {
            allSoucoupes.splice(i,1);
            i = i-1;
			if(compteur<3){
				affiche_score=affiche_score-1000;
				score.textContent = affiche_score;	
				compteur+=1;
			}
			if (compteur==3){
				window.removeEventListener("keydown",keyAction);
				document.getElementById("nouvelleSoucoupe").removeEventListener("click",addSoucoupe);
				arret_soucoupe();
				infini.removeEventListener('click',addSoucoupe2);
				score.innerHTML="Perdu !";
			}
        }
    }
    window.requestAnimationFrame(moveAndDrawSoucoupes);
}

var collision_soucoupe_sort = function(soucoupe) {
	//Renvoie True si l'image de la soucoupe est sortie de la gauche du canvas
    return sortie_soucoupe(soucoupe.xs);
}

var sortie_soucoupe = function(xs) {
   // Renvoie True si l'abscisse de l'image de la soucoupe est <0
   return (xs<0)
}

var collision = function (tir,soucoupe){
	//Renvoie True si il y a collision entre les rectangles délimitant les images de chacun de ces objets, le résultat est false sinon. 
	return((tir.x_tir > soucoupe.xs) && (tir.x_tir < soucoupe.xs+soucoupeImg.width) &&(tir.y_tir > soucoupe.ys) && (tir.y_tir < soucoupe.ys+soucoupeImg.height));
}
	
var tirReussi = function (t){
	  /*Si il y a collision entre t et l'une au moins des soucoupes volantes alors cette fonction a pour 
		résultat une soucoupe volante en collision avec ce tir, sinon le résultat est undefined ou null. */
	for (i=0 ; i<allSoucoupes.length ; i++){
		if (collision (t, allSoucoupes[i])){
			return allSoucoupes[i];
		}
	}
	return undefined;
}

var addSoucoupe2=function(){
	//crée une nouvelle soucoupe volante à intervalle régulier (toutes les 750ms).
	ctrltemp=window.setInterval(addSoucoupe,750);
	infini.removeEventListener('click',addSoucoupe2);
	infini.addEventListener('click',arret_soucoupe);
}

var arret_soucoupe=function(){
	// interrompt l'arrivée de nouvelles soucoupes, jusqu'au prochain clic sur le même bouton
	window.clearInterval(ctrltemp);
	infini.removeEventListener('click',arret_soucoupe);
	infini.addEventListener('click',addSoucoupe2);
}