
const textarea = document.getElementById('comment');
const charCount = document.getElementById('char-count');
const resetButton = document.getElementById('reset-button');

textarea.addEventListener('input', function () {
    const maxLength = 300;
    const currentLength = textarea.value.length;
    const remaining = maxLength - currentLength;

    if (remaining >= 0) {
        charCount.textContent = `Characters remaining: ${remaining}`;
    } else {
        charCount.textContent = `Character Exceeded`;
        textarea.value = textarea.value.slice(0, maxLength); // Truncate excess characters
    }
});

resetButton.addEventListener('click', function () {
charCount.textContent = `Characters remaining: 300`;
});
