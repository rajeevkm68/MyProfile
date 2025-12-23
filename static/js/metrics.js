document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".metric-value");

  counters.forEach(counter => {
    const target = +counter.dataset.value;
    const duration = 900; // subtle
    const startTime = performance.now();

    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = Math.floor(progress * target);

      counter.textContent = value;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        counter.textContent = target;
      }
    }

    requestAnimationFrame(update);
  });
});
