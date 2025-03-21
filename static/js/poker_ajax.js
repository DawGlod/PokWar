function call() {
    const button = document.getElementById("call-button");
    fetch('/poker', {
        method: 'POST',
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
        }     
    })
    .catch(error => console.error('Error:', error));
}

function fold() {
    const button = document.getElementById("fold-button");
    fetch('/poker', {
        method: 'POST',
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
        }     
    })
    .catch(error => console.error('Error:', error));
}