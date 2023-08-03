// Set the date of 4th August 2023 at 5:00 PM (months are 0-indexed, hours are 0-23 indexed)
const targetDate = new Date(2023, 7, 4, 17, 0, 0);

function updateCountdown() {
  const now = new Date();
  const timeRemaining = targetDate - now;

  if (timeRemaining <= 0) {
    document.getElementById("countdown").innerHTML = "Countdown expired!";
  } else {
    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor(
      (timeRemaining % (1000 * 60 * 60)) / (1000 * 60)
    );
    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    document.getElementById(
      "countdown"
    ).innerHTML = `${hours} hours, ${minutes} minutes, ${seconds} seconds`;
  }
}

// Update the countdown every second
setInterval(updateCountdown, 1000);
