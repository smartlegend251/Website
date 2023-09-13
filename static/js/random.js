function rand5() {
    // Generate a random 5-digit number
    const randomNumber = Math.floor(10000 + Math.random() * 90000);

    // Set the generated number in the input field
    document.getElementById('rand5d').value = randomNumber;
}