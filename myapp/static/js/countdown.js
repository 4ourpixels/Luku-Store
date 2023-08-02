// Set the date of 4th August 2023 (months are 0-indexed)
const targetDate = new Date(2023, 7, 4);

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
    ).innerHTML = `${days} day, ${hours} hours, ${minutes} minutes, ${seconds} seconds`;
  }
}

// Update the countdown every second
setInterval(updateCountdown, 1000);
