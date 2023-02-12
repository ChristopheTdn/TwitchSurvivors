class Survivant {
	// JSON to Object
	constructor(name, career, prestige, credit, levelWeapon, levelArmor, levelTransport, levelGear, raidType, raidDistance, aids, dead, hurt, imgCar) {
		this.name = name;
		this.career = career;
		this.prestige = prestige;
		this.credit = credit;
		this.levelWeapon = levelWeapon;
		this.levelArmor = levelArmor;
		this.levelTransport = levelTransport;
		this.levelGear = levelGear;
		this.raidType = raidType;
		this.raidDistance = raidDistance;
		this.aids = aids;
		this.dead = dead;
		this.hurt = hurt;
		this.imgCar = imgCar;
		this.box = document.createElement('div');
		this.p = document.createElement('p');
		this.img = document.createElement('img');
		this.badge = document.createElement('img');
		this.status = document.createElement('img');
		this.pAids = document.createElement('p');
		this.pseudoBox = document.createElement('div');
	}

	setTemplate() {
		this.box.classList.add("cars");
		this.box.id = this.name;
		this.setRenforts();
		this.box.appendChild(this.pseudoBox);
		this.pseudoBox.classList.add('pseudoBox')
		this.setBadge();
		this.setStatus();
		this.setImg();
		this.setPseudo();
		this.setPosition();

		document.getElementById('line').appendChild(this.box)
	}

	// Si le survivant est en vie : affiche la voiture via son niveau en véhicule
	// Sinon, affiche une image de fail
	setImg() {
			this.img.setAttribute('src', '../assets/img/cars/'+this.imgCar);
			this.img.style.width = (config.sizes.cars.car*100)+"px";
			this.box.appendChild(this.img);
	}

	//
	setStatus() {
		if(this.dead) {
			this.status.setAttribute('src', '../assets/img/badges/skull.png');
			this.status.classList.add('badge')
			this.pseudoBox.appendChild(this.status);
		} else {
			if(this.hurt) {
				this.status.setAttribute('src', '../assets/img/badges/blood.png');
				this.status.classList.add('badge')
				this.pseudoBox.appendChild(this.status);
			}
		}
	}

	//
	setBadge() {
			this.badge.setAttribute('src', '../assets/img/badges/'+this.raidType+'.png');
			this.badge.classList.add('badge')
			this.pseudoBox.appendChild(this.badge);
	}

	// ¯\_(ツ)_/¯
	setPseudo(){
		this.p.innerHTML = this.name;
		this.p.style.fontSize = config.sizes.cars.pseudo+'em';
		this.p.style.fontFamily = config.font.name;
		this.p.style.color = config.colors.pseudo_cars;
		this.p.style.fontWeight = config.font_weight.pseudo_cars;
		this.p.classList.add("pseudo");
		this.pseudoBox.appendChild(this.p);
	}

	// Construction de la ligne renforts
	setRenforts(){
		if(Object.keys(this.aids).length > 0) {
			this.pAids.innerHTML = "( ";
			for (var i = 0 ; i <= Object.values(this.pAids).length ; i++) {
				this.pAids.innerHTML += Object.values(this.aids)[i];
				if( i !== Object.values(this.aids).length -1) {
					this.pAids.innerHTML += " - ";
				}
			}
			this.pAids.innerHTML += " )";
			this.pAids.style.fontSize = config.sizes.cars.aids+'em';
			this.pAids.style.fontFamily = config.font.name;
			this.pAids.style.color = config.colors.pseudo_aids;
			this.pAids.classList.add('renforts')
			this.box.appendChild(this.pAids);
		}
	}

	// définition position et orientation
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

	// Import the font define in front.ini
	let font = new FontFace(config.font.name, "url(../assets/fonts/"+config.font.file+")");
	document.fonts.add(font);

	let survivants = [];

	fetch('../raid.json')
	.then((response) => response.json())
	.then((jsonSurvivants) => {
		for (let jsonSurvivant in jsonSurvivants) {
			let survivant = new Survivant(
				jsonSurvivants[jsonSurvivant].NAME,
				jsonSurvivants[jsonSurvivant].STATS.career,
				jsonSurvivants[jsonSurvivant].STATS.prestige,
				jsonSurvivants[jsonSurvivant].STATS.credit,
				jsonSurvivants[jsonSurvivant].STATS.level_weapon,
				jsonSurvivants[jsonSurvivant].STATS.level_armor,
				jsonSurvivants[jsonSurvivant].STATS.level_transport,
				jsonSurvivants[jsonSurvivant].STATS.level_gear,
				jsonSurvivants[jsonSurvivant].TYPE,
				jsonSurvivants[jsonSurvivant].DISTANCE,
				jsonSurvivants[jsonSurvivant].RENFORT,
				jsonSurvivants[jsonSurvivant].DEAD,
				jsonSurvivants[jsonSurvivant].HURT,
				jsonSurvivants[jsonSurvivant].GFX_CAR,
			)
			survivants[survivant.name] = survivant;
			survivant.setTemplate();
		}
	});
})