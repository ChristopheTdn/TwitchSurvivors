const SURVIVORS = [];

class Survivant {
	// JSON to Object
	constructor(name, career, prestige, credit, levelWeapon, levelArmor, levelTransport, levelGear, raidType, raidDistance, aids, dead, hurt, visi, imgCar) {
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
		this.visi = visi;
		this.imgCar = imgCar;
		this.gap = 0;
		this.box = document.createElement('div');
		this.p = document.createElement('p');
		this.img = document.createElement('img');
		this.badge = document.createElement('img');
		this.status = document.createElement('img');
		this.pAids = document.createElement('p');
		this.pseudoBox = document.createElement('div');
		this.line = document.createElement('div');
	}

	setTemplate() {
		this.box.classList.add("cars");
		this.box.id = this.name;
		if(this.visi == 1) {
			this.setRenforts();
			this.box.appendChild(this.pseudoBox);
			this.box.appendChild(this.line);
			this.pseudoBox.classList.add('pseudoBox')
			this.setPseudo();
		}
		this.setBadge();
		this.setStatus();
		this.setImg();
		this.setPosition();

		document.getElementById('line').appendChild(this.box)
	}

	setImg() {
			this.img.setAttribute('src', '../assets/img/cars/'+this.imgCar);
			this.img.style.width = (config.cars.car_size*100)+"px";
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
		this.p.style.fontSize = config.carspseudo_size+'em';
		this.p.style.fontFamily = config.font.name;
		this.p.style.color = config.cars.pseudo_color;
		this.p.style.fontWeight = config.cars.pseudo_cars;
		this.p.classList.add("pseudo");
		this.pseudoBox.appendChild(this.p);
	}

	// Construction de la ligne renforts
	setRenforts(){
		if(this.aids !== "") {
			this.pAids.innerHTML = "( ";
			this.pAids.innerHTML += this.aids;
			this.pAids.innerHTML += " )";
			this.pAids.style.fontSize = config.cars.aid_size+'em';
			this.pAids.style.fontFamily = config.font.name;
			this.pAids.style.color = config.cars.aid_color;
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
		this.setSuperposition();
	}

	setSuperposition() {
		for (let survivor in SURVIVORS) {
			if(this.name !== SURVIVORS[survivor].name) {
				let raiderOneDistance = this.raidDistance;
				let raiderTwoDistance = SURVIVORS[survivor].raidDistance;
				if( 
					((raiderOneDistance - raiderTwoDistance) <= 2 && (raiderTwoDistance - raiderOneDistance) <= 2) 
				|| 
					((raiderOneDistance + raiderTwoDistance) >= 98 && (raiderOneDistance + raiderTwoDistance) <= 102)
					) {

					if(this.gap === SURVIVORS[survivor].gap) {
						if(SURVIVORS[survivor].visi) {
							this.gap += config.cars.gap_size;
							this.line.style.height = this.gap+"em";
							this.line.style.height = this.gap+"em";
							this.line.classList.add('car-line');
							this.line.style.background = config.cars.line_color;
							this.pseudoBox.style.paddingBottom = "0em";
						}
					}
				}
			}
		}
	}
} 

// Requête au JSON et construction de Survivant
async function afficheRaid() {
	document.getElementById("line").innerHTML = "";
	// Import the font define in front.ini
	let font = new FontFace(config.font.name, "url(../assets/fonts/"+config.font.file+")");
	document.fonts.add(font);

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
				jsonSurvivants[jsonSurvivant].VISI,
				jsonSurvivants[jsonSurvivant].GFX_CAR,
			)
			SURVIVORS[survivant.name] = survivant;
			survivant.setTemplate();
		}
	});
}
setInterval(afficheRaid, 10000);
afficheRaid();