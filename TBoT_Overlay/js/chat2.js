class Chat {
	constructor(list) {
		this.list = list;
	}

	display() {
		let box = document.getElementById('box');
		// this.list.length = 22;
		this.list.reverse();
		console.log(this.list)
		for (let i = 0; i < this.list.length; i++) {
			let message = document.createElement('p');
			message.innerHTML = list[i].content;
			message.id = list[i].id
			message.classList.add('message');
			box.insertBefore(message, box.lastChild);
		}
	}
}


class Message {
	constructor(id, content, date) {
		this.id = id;
		this.content = content;
		this.date = date;
		this.messageP = document.createElement('p');
	}

	setMessage() {
		
		this.messageP.classList.add('message');
		this.messageP.id = this.id;
		this.messageP.innerHTML = this.content;
		// setOpacity();
	}

	setOpacity() {

	}
}

let list = [];
fetch('chat.json')
		.then((response) => response.json())
		.then((messages) => {
			for (message in messages) {
				
				let newMessage = new Message(message, messages[message], new Date())
				if (!list[newMessage.id]) {
					list[newMessage.id] = newMessage;
					newMessage.setMessage();
				}
			}
			let chat = new Chat(list);
			chat.display();
		})