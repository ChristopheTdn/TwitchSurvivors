class Chat {
	constructor() {
		this.box = document.getElementById('box');
	}

	insert(p) {
		this.box.style.fontFamily
		this.box.insertBefore(p, this.box.firstChild);
	}
	setOpacity() {
		let messages = this.box.children;
		if(messages.length > 20) {
			for (let i = 0; i < 6; i++) {
				if(i < 3) {
					messages[i].style.opacity = 0.3;
				} else {
					messages[i].style.opacity = 0.6;
				}
			}
		}
	}
}

class Message {
	constructor(content) {
		this.content = content;
		this.p = document.createElement('p');
		this.p.classList.add('message');
	}

	display() {
		let chat = new Chat();
		this.p.innerHTML = this.content;
		this.p.style.fontFamily = config.font.name;
		this.p.style.fontSize = config.sizes.chat.text_size+"em";
		chat.insert(this.p);
		if(this.p.firstElementChild){
			this.p.firstElementChild.style.color = config.colors.pseudo_chat
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
				let message = new Message(list[i]);
				if(message.content !=="") {
					message.display();
				}
			}
			let chat = new Chat();
			chat.setOpacity();
		})
})