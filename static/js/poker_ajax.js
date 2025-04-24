function call() {
    fetch('/poker', {
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
        } 
        else if (data.counter == 1){
            document.getElementById('card1').src = `/static/${data.card1_image}`;
            document.getElementById('card2').src = `/static/${data.card2_image}`;
            document.getElementById('card3').src = `/static/${data.card3_image}`;
        }

        else if (data.counter == 2){
            document.getElementById('card4').src = `/static/${data.card4_image}`;
        }  
        
        else if (data.counter == 3){
            document.getElementById('card5').src = `/static/${data.card5_image}`;
        } 

        else if (data.counter == 4){
            document.getElementById('my-comb').innerText = `${data.my_comb}`;
            document.getElementById('enemy-comb').innerText = `${data.enemy_comb}`;
            document.getElementById('my-result').innerText = `${data.my_result}`;
            document.getElementById('enemy-result').innerText = `${data.enemy_result}`;
            document.getElementById('enemy_card1_image').src = `/static/${data.enemy_card1_image}`;
            document.getElementById('enemy_card2_image').src = `/static/${data.enemy_card2_image}`;

            buttonsDisable()
            restartGame()
        }     
    })
    .catch(error => console.error('Error:', error));
}

function fold() {
    fetch('/poker', {
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
        } 
        else{
            document.getElementById('card1').src = `/static/${data.card1_image}`;
            document.getElementById('card2').src = `/static/${data.card2_image}`;
            document.getElementById('card3').src = `/static/${data.card3_image}`;
            document.getElementById('card4').src = `/static/${data.card4_image}`;     
            document.getElementById('card5').src = `/static/${data.card5_image}`;
            document.getElementById('my-comb').innerText = `${data.my_comb}`;
            document.getElementById('enemy-comb').innerText = `${data.enemy_comb}`;
            document.getElementById('my-result').innerText = `LOSE`;
            document.getElementById('enemy-result').innerText = `WIN`;
            document.getElementById('enemy_card1_image').src = `/static/${data.enemy_card1_image}`;
            document.getElementById('enemy_card2_image').src = `/static/${data.enemy_card2_image}`;

            buttonsDisable()
            restartGame()
        }     
    })
    .catch(error => console.error('Error:', error));
}

function buttonsDisable() {
    const foldButton = document.getElementById("fold-button");
    const callButton = document.getElementById("call-button");
    const raiseButton = document.getElementById("raise-button");
    
    foldButton.disabled=true;
    callButton.disabled=true;
    raiseButton.disabled=true;

    setTimeout(function() {
        foldButton.disabled=false;
        callButton.disabled=false;
        raiseButton.disabled=false;
    }, 2000)
}

function restartGame() {
    setTimeout(function() {
        fetch('/restart-poker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('card1').src = `/static/images/cards/green_back.png`;
            document.getElementById('card2').src = `/static/images/cards/green_back.png`;
            document.getElementById('card3').src = `/static/images/cards/green_back.png`;
            document.getElementById('card4').src = `/static/images/cards/green_back.png`;
            document.getElementById('card5').src = `/static/images/cards/green_back.png`;
            document.getElementById('my_card1_image').src = `/static/${data.my_card1_image}`;
            document.getElementById('my_card2_image').src = `/static/${data.my_card2_image}`;
            document.getElementById('enemy_card1_image').src = `/static/images/cards/green_back.png`;
            document.getElementById('enemy_card2_image').src = `/static/images/cards/green_back.png`;
            document.getElementById('my-balance').innerText = data.my_balance;
            document.getElementById('enemy-balance').innerText = data.enemy_balance;

            document.getElementById('my-comb').innerHTML = '&nbsp;';
            document.getElementById('enemy-comb').innerHTML = '&nbsp;';
            document.getElementById('my-result').innerHTML = '&nbsp;';
            document.getElementById('enemy-result').innerHTML = '&nbsp;';
        });
    }, 8000);
}