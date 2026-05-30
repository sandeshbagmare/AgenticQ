const revealItems = document.querySelectorAll("[data-reveal]");

revealItems.forEach((item, index) => {
  item.style.animationDelay = `${index * 120}ms`;
});

const year = document.getElementById("year");
if (year) {
  year.textContent = String(new Date().getFullYear());
}
