class Chat {
	constructor() {
		this.box = document.getElementById('box');
		this.alignment = config.chat.alignment;
		this.textAlignment = config.chat.text_alignment;
		this.display();

	}

	display() {
		this.box.style.border = config.chat.border_size+"px solid "+config.chat.border_color;
		this.box.style.background = config.chat.background;
		this.box.style.padding = config.chat.margin+"em";
		this.box.style.borderRadius = config.chat.border_radius+"em";

		let body = document.querySelector('body');
		switch (this.alignment) {
			case  "left":
			body.style.marginRight = "auto";	
			break;
			case "right": 
			body.style.marginLeft = "auto";	
			break;
		}
		switch (this.textAlignment) {
			case  "left":
			this.box.style.textAlign = "left";	
			break;
			case "right": 
			this.box.style.textAlign = "right";
			break;
		}
	}

	insert(p) {
		this.box.style.fontFamily
		this.box.insertBefore(p, this.box.firstChild);
	}
}

class Message {
	constructor(content, date) {
		this.content = content;
		let currentDate = new Date();
		let timestamp = currentDate.getTime();
		this.date = date;
		this.isInDelay = this.setIsInDelay(timestamp);
		this.p = document.createElement('p');
		this.p.classList.add('message');
	}

	display(chat) {
		let currentDate = new Date();
		let timestamp = currentDate.getTime();
		this.p.innerHTML = this.content;
		this.p.style.fontFamily = config.font.name;
		this.p.style.fontSize = config.chat.text_size+"em";
		this.p.style.lineHeight = config.chat.line_spacing+"em";
		if(this.isInDelay) {
			this.setOpacity();
			chat.insert(this.p);
			this.p.style.color = config.chat.text_color;
			this.p.style.weight = config.chat.text_weight;
			if(this.p.firstElementChild){
				this.p.firstElementChild.style.color = config.chat.pseudo_color;
				this.p.firstElementChild.style.fontWeight = config.chat.pseudo_weight;
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
		let configTime = config.chat.delay_to_display*1000;
		if((timestamp - this.date) < (0.33*configTime)) {
			this.p.style.opacity = 1;
		} else {
			if((timestamp - this.date) < (0.66*configTime)) {
				this.p.style.opacity = 0.6;
			} else {
					this.p.style.opacity = 0.0;
			}
		}
	}
}

window.addEventListener('load', (event) => {

	// Import the font define in front.ini
	let font = new FontFace(config.font.name, "url(../assets/fonts/"+config.font.file+")");
	document.fonts.add(font);

	document.body.style.width = config.chat.width;
	document.body.style.height = config.chat.height;

	fetch('../chat.json')
		.then((response) => response.json())
		.then((messages) => {

			list = Object.values(messages);
			let chat = new Chat();
			for (let i = 0; i < list.length; i++) {
				let message = new Message(list[i].message, list[i].date);
				if(message.content !=="") {
					message.display(chat);
				}
			}
		})
})
