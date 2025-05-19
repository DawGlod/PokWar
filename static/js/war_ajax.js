function playNextCard() {
    const button = document.getElementById("play-button");
    fetch('/war/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'redirect') {
            window.location.href = data.url;
        } else {
            document.getElementById('my-hand-count').innerText = `My hand: ${data.my_hand} cards`;
            document.getElementById('enemy-hand-count').innerText = `Enemy hand: ${data.enemy_hand} cards`;
            document.getElementById('my-first').src = `/static/${data.my_card_image}`;
            document.getElementById('enemy-first').src = `/static/${data.enemy_card_image}`;

            const gameName = document.querySelector('.gamename');

            if (data.war_status == true) {
                gameName.classList.add('war-active');
            } else {
                gameName.classList.remove('war-active');
            }
        }
    })
    .catch(error => console.error('Error:', error));
    
    button.disabled=true;
    
    setTimeout(function() {
        button.disabled=false;
    }, 200)
}