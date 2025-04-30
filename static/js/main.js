setTimeout(() => {
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    alert.classList.add('fade-out');
    setTimeout(() => alert.remove(), 500); // remove after fade
});
}, 2000);
