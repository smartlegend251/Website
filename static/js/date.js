// const dateInput  = document.getElementById('date')
// const currentDate = new Date();
//     const formattedDate = currentDate.toISOString().split('T')[0];
//     dateInput.value = formattedDate;

const dateInput = document.getElementById('date');
const timeInput = document.getElementById('time');
const currentDate = new Date();

// Get the date in "YYYY-MM-DD" format
const formattedDate = currentDate.toISOString().split('T')[0];

// Get the time in "HH:MM" format
const formattedTime = currentDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

dateInput.value = formattedDate; // Set the date input
timeInput.value = formattedTime; // Set the time input
