let survivants = {};

placeCars();
setInterval("placeCars()", 10000);

function placeCars() {

	let line = document.getElementById('line');
	line.innerHTML = "";

	fetch('assets/raid.json')
	    .then((response) => response.json())
	    .then((survivants) => {
	    	for (let survivant in survivants) {

			let div = document.createElement('div');
			let p = document.createElement('p');
			let img = document.createElement('img');
			let pRenforts = document.createElement('p');
				
			if(JSON.stringify(survivants[survivant].RENFORT) !== '{}') {
				pRenforts.classList.add("renforts");
				pRenforts.innerHTML = "( ";

				for (let renfort in survivants[survivant].RENFORT) {
					pRenforts.innerHTML += survivants[survivant].RENFORT[renfort];

					let values = Object.values(survivants[survivant].RENFORT);

					if(survivants[survivant].RENFORT[renfort] !== values[values.length -1] ) {
						pRenforts.innerHTML += " - ";
					}
				}
				pRenforts.innerHTML += " )";
			}

			div.appendChild(pRenforts);
			
			div.classList.add('cars');
			div.id = survivants[survivant].NAME;
			let position = survivants[survivant].DISTANCE;
			let cssPosition = 0;
			if(position == 50) {
				cssPosition = 100;
			} else if (position > 50){
				cssPosition = (100-position)*2;
				img.classList.add('rotate');
			} else if (position < 50) {
				cssPosition = position*2;
			}
				div.style.left = (cssPosition-5)+"%";

			p.classList.add('pseudo');
			p.innerHTML = survivants[survivant].NAME

			img.setAttribute('src', 'assets/cars/'+survivants[survivant]["STATS"].levelCar+'.png');

			div.appendChild(p);
			div.appendChild(img);

			let line = document.getElementById('line');
			line.appendChild(div);
		}
	});
}
