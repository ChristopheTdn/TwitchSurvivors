// Obtenir l'élément "box"
let box = document.getElementById("box");
displayMessages()
setInterval("displayMessages()", 1000)

function displayMessages() {

fetch('assets/chat.json')
	    .then((response) => response.json())
	    .then((messages) => {
			
			for (message in messages) {

				if(document.getElementById(message) === null) {

					let messageP = document.createElement('p');
					messageP.classList.add('message');
					messageP.id = message;
					messageP.innerHTML = messages[message];

					messageP.style.opacity = 0;
					
					box.insertBefore(messageP, box.lastChild);

					setTimeout(() => {
						messageP.style.opacity = 1;
					  }, 50);
				}
			}
		})
}