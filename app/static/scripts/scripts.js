// document.addEventListener('DOMContentLoaded', function() {
//     const calendarElement = document.getElementById('calendar');
//     const events = JSON.parse(calendarElement.getAttribute('data-events'));

//     events.forEach(event => {
//         const eventDate = new Date(event.date);
//         const day = eventDate.getDate();
//         const month = eventDate.getMonth();
//         const year = eventDate.getFullYear();

//         const bubble = document.createElement('div');
//         bubble.className = 'event-bubble';
//         bubble.innerText = event.title;

//         const dayElement = calendarElement.querySelector(`.day[data-day="${day}"][data-month="${month}"][data-year="${year}"]`);
//         if (dayElement) {
//             dayElement.appendChild(bubble);
//         }
//     });
// });