class Survivant {
	// JSON to Object
	constructor(name, reputation, levelGun, levelWear, levelCar, raidType, raidDistance, raidRenforts, alive) {
		this.name = name;
		this.reputation = reputation;
		this.levelGun = levelGun;
		this.levelWear = levelWear;
		this.levelCar = levelCar;
		this.raidType = raidType;
		this.raidDistance = raidDistance;
		this.raidRenforts = raidRenforts;
		this.alive = alive;
		this.box = document.createElement('div');
		this.p = document.createElement('p');
		this.img = document.createElement('img');
		this.pRenforts = document.createElement('p');
	}

	setTemplate() {
		this.box.classList.add("cars");
		this.box.id = this.name;
		this.p.classList.add("pseudo");
		this.pRenforts.classList.add('renforts')
		this.box.appendChild(this.pRenforts);
		this.box.appendChild(this.p);
		this.box.appendChild(this.img);
		this.setImg();
		this.setPseudo();
		this.setRenforts();
		this.setPosition();

		document.getElementById('line').appendChild(this.box)
	}

	// Si le survivant est en vie : affiche la voiture via son niveau en véhicule
	// Sinon, affiche une image de fail
	// A voir = délai d'affichage décés ? comparer date du décés ? 
	// A voir = randomiser l'affichage ?
	setImg() {
		if(this.alive === true) {
			this.img.setAttribute('src', 'assets/cars/'+this.levelCar+'.png');
		} else {
			this.img.setAttribute('src', 'assets/cars/fail-1.png')
		}
	}

	// ¯\_(ツ)_/¯
	setPseudo(){
		this.p.innerHTML = this.name;
	}

	// Construction de la ligne renforts
	setRenforts(){
		if(JSON.stringify(this.raidRenforts) !== "{}") {
			this.pRenforts.innerHTML = "( ";
			for (var i = 0 ; i < Object.values(this.raidRenforts).length ; i++) {
				this.pRenforts.innerHTML += Object.values(this.raidRenforts)[i];
				if( i !== Object.values(this.raidRenforts).length -1) {
					this.pRenforts.innerHTML += " - ";
				}
			}
			this.pRenforts.innerHTML += " )";
		}
	}

	// définition position et orientation
	// croissant ou décroissant ?
	setPosition(){
		var cssPosition;
		if (this.raidDistance == 50) {
			cssPosition = 100;
		} else if (this.raidDistance > 50) {
			cssPosition = (100 - this.raidDistance) * 2;
		} else if (this.raidDistance < 50) {
			this.img.classList.add('rotate');
			cssPosition = this.raidDistance * 2;
		}
		this.box.style.left = (cssPosition - 5) + "%";
	}
}

// Requête au JSON et construction de Survivant
window.addEventListener('load', (event) => {
	let survivants = [];

	fetch('assets/raid.json')
	.then((response) => response.json())
	.then((jsonSurvivants) => {
		for (let jsonSurvivant in jsonSurvivants) {
			let survivant = new Survivant(
				jsonSurvivants[jsonSurvivant].NAME,
				jsonSurvivants[jsonSurvivant].STATS.reputation,
				jsonSurvivants[jsonSurvivant].STATS.levelGun,
				jsonSurvivants[jsonSurvivant].STATS.levelWear,
				jsonSurvivants[jsonSurvivant].STATS.levelCar,
				jsonSurvivants[jsonSurvivant].TYPE,
				jsonSurvivants[jsonSurvivant].DISTANCE,
				jsonSurvivants[jsonSurvivant].RENFORT,
				jsonSurvivants[jsonSurvivant].ALIVE,
			)
			survivants[survivant.name] = survivant;
			survivant.setTemplate();
		}
	});
})
