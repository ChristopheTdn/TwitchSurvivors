class Chat {
	constructor() {
		this.box = document.getElementById('box');
	}

	insert(p) {
		this.box.style.fontFamily
		this.box.insertBefore(p, this.box.firstChild);
	}
}

class Message {
	constructor(content, date) {
		this.content = content;
		this.date = date;
		this.isInDelay = this.setIsInDelay(date);
		console.log(this.isInDelay)
		this.p = document.createElement('p');
		this.p.classList.add('message');
	}

	display() {
		let chat = new Chat();
		this.p.innerHTML = this.content;
		this.p.style.fontFamily = config.font.name;
		this.p.style.fontSize = config.sizes.chat.text_size+"em";
		if(this.isInDelay) {
			this.setOpacity();
			chat.insert(this.p);
			if(this.p.firstElementChild){
				this.p.firstElementChild.style.color = config.colors.pseudo_chat
			}
		}
	}

	setIsInDelay(date) {
		let currentDate = new Date();
		let timestamp = currentDate.getTime();
		if((timestamp - date) > config.chat.delay_to_display) {
			return false;
		} else {
			return true;
		}
	}

	setOpacity() {
		let currentDate = new Date();
		let timestamp = currentDate.getTime();
		if((timestamp - this.date) > (0.33*config.chat.delay_to_display)) {
			this.p.style.opacity = 0.6;
		}
		if((timestamp - this.date) > (0.66*config.chat.delay_to_display)) {
			this.p.style.opacity = 0.3;
		}
		if((timestamp - this.date) > (0.99*config.chat.delay_to_display)) {
			this.p.style.opacity = 0.1;
		}
	}
}

window.addEventListener('load', (event) => {

	// Import the font define in front.ini
	let font = new FontFace(config.font.name, "url(../assets/fonts/"+config.font.file+")");
	document.fonts.add(font);

	document.body.style.width = config.sizes.chat.width;
	document.body.style.height = config.sizes.chat.height;

	fetch('../chat.json')
		.then((response) => response.json())
		.then((messages) => {

			list = Object.values(messages);

			for (let i = 0; i < list.length; i++) {
				let message = new Message(list[i].message, list[i].date);
				if(message.content !=="") {
					message.display();
				}
			}
		})
})