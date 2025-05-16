function call() {
    let myBalance = parseInt(document.getElementById('my-balance').textContent)
    let enemyBalance = parseInt(document.getElementById('enemy-balance').textContent)
    let totalPot = parseInt(document.getElementById('total-pot').textContent)
    
    fetch('/poker/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.counter == 1){
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

        else if (data.counter >= 4){
            document.getElementById('my-comb').innerText = `${data.my_comb}`;
            document.getElementById('enemy-comb').innerText = `${data.enemy_comb}`;
            document.getElementById('total-pot').innerText = `${data.my_result}`;
            document.getElementById('enemy-result').innerText = `${data.enemy_result}`;
            document.getElementById('enemy_card1_image').src = `/static/${data.enemy_card1_image}`;
            document.getElementById('enemy_card2_image').src = `/static/${data.enemy_card2_image}`;

            buttonsDisable()           
            
            if (data.my_result == 'WIN') 
                myBalance += totalPot
            else if (data.my_result == 'LOSE') 
                enemyBalance += totalPot
            else if (data.my_result == 'DRAW') {
                myBalance += totalPot / 2
                enemyBalance += totalPot / 2
            }

            const maxRaise = Math.min(myBalance, enemyBalance)
            
            fetch('/poker/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({
                    'my_balance': myBalance,
                    'enemy_balance': enemyBalance,
                    'max_raise': maxRaise
                })
            })
            .then(() => restartGame())
        }     
    })
    .catch(error => console.error('Error:', error));
}

function fold() {
    let myBalance = parseInt(document.getElementById('my-balance').textContent)
    let enemyBalance = parseInt(document.getElementById('enemy-balance').textContent)
    let totalPot = parseInt(document.getElementById('total-pot').textContent)

    fetch('/poker/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('card1').src = `/static/${data.card1_image}`;
        document.getElementById('card2').src = `/static/${data.card2_image}`;
        document.getElementById('card3').src = `/static/${data.card3_image}`;
        document.getElementById('card4').src = `/static/${data.card4_image}`;     
        document.getElementById('card5').src = `/static/${data.card5_image}`;
        document.getElementById('my-comb').innerText = `${data.my_comb}`;
        document.getElementById('enemy-comb').innerText = `${data.enemy_comb}`;
        document.getElementById('total-pot').innerText = `LOSE`;
        document.getElementById('enemy-result').innerText = `WIN`;
        document.getElementById('enemy_card1_image').src = `/static/${data.enemy_card1_image}`;
        document.getElementById('enemy_card2_image').src = `/static/${data.enemy_card2_image}`;

        buttonsDisable()

        enemyBalance += totalPot
        const maxRaise = Math.min(myBalance, enemyBalance)
       
        fetch('/poker/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                'my_balance': myBalance,
                'enemy_balance': enemyBalance,
                'max_raise': maxRaise
            })
        })
        .then(() => restartGame())         
    })
    .catch(error => console.error('Error:', error));
}

function raise() {
    let myBalance = parseInt(document.getElementById('my-balance').textContent)
    let enemyBalance = parseInt(document.getElementById('enemy-balance').textContent)
    let raiseValue = parseInt(document.getElementById('raise-value').textContent)
    let totalPot = parseInt(document.getElementById('total-pot').textContent)
    
    totalPot += raiseValue * 2
    myBalance -= raiseValue
    enemyBalance -= raiseValue

    const maxRaise = Math.min(myBalance, enemyBalance)
    
    fetch('/poker/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({
            'my_balance': myBalance,
            'enemy_balance': enemyBalance,
            'max_raise': maxRaise,
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('my-balance').textContent = myBalance
        document.getElementById('enemy-balance').textContent = enemyBalance
        document.getElementById('raise-slider').max = maxRaise
        document.getElementById('total-pot').textContent = totalPot
        
        if (maxRaise >= 50) {
            document.getElementById('raise-slider').value = 50
            document.getElementById('raise-value').textContent = 50
        }
        else {
            document.getElementById('raise-slider').value = maxRaise
            document.getElementById('raise-value').textContent = maxRaise
        }

        if (Math.min(myBalance, enemyBalance) <= 0) {
            data.counter = 4
        }

        if (data.counter == 1){
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
        else if (data.counter >= 4 ){
            document.getElementById('my-comb').innerText = `${data.my_comb}`;
            document.getElementById('enemy-comb').innerText = `${data.enemy_comb}`;
            document.getElementById('total-pot').innerText = `${data.my_result}`;
            document.getElementById('enemy-result').innerText = `${data.enemy_result}`;
            document.getElementById('enemy_card1_image').src = `/static/${data.enemy_card1_image}`;
            document.getElementById('enemy_card2_image').src = `/static/${data.enemy_card2_image}`;
            document.getElementById('card1').src = `/static/${data.card1_image}`;
            document.getElementById('card2').src = `/static/${data.card2_image}`;
            document.getElementById('card3').src = `/static/${data.card3_image}`;
            document.getElementById('card4').src = `/static/${data.card4_image}`;            
            document.getElementById('card5').src = `/static/${data.card5_image}`;

            buttonsDisable()
            
            if (myBalance === 0 && data.my_result === 'LOSE') {
                setTimeout(() => {
                    window.location.href = '/defeat';
                }, 8000)
            } 
            else if (enemyBalance === 0 && data.my_result === 'WIN') {
                setTimeout(() => {
                    window.location.href = '/victory';
                }, 8000)
            }
            else {
                if (data.my_result == 'WIN') 
                    myBalance += totalPot
                else if (data.my_result == 'LOSE') 
                    enemyBalance += totalPot
                else if (data.my_result == 'DRAW') {
                    myBalance += totalPot / 2
                    enemyBalance += totalPot / 2
                }
                
                const maxRaise = Math.min(myBalance, enemyBalance)

                fetch('/poker/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    body: JSON.stringify({
                        'my_balance': myBalance,
                        'enemy_balance': enemyBalance,
                        'max_raise': maxRaise
                    })
                })
                .then(() => restartGame())  
            }     
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
    }, 8000)
}

function restartGame() {
    setTimeout(function() {
        fetch('/restart-poker/', {
            method: 'PUT',
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
            document.getElementById('raise-slider').max = data.max_raise;

            document.getElementById('my-comb').innerHTML = '&nbsp;';
            document.getElementById('enemy-comb').innerHTML = '&nbsp;';
            document.getElementById('total-pot').innerText = data.total_pot;
            document.getElementById('enemy-result').innerHTML = '&nbsp;';
        });
    }, 8000);
}

function initRaiseSlider() {
    const slider = document.getElementById('raise-slider');
    const valueDisplay = document.getElementById('raise-value');

    if (slider && valueDisplay) {
        slider.addEventListener('input', () => {
            valueDisplay.innerText = slider.value;
        });
    }
}

document.addEventListener('DOMContentLoaded', initRaiseSlider);