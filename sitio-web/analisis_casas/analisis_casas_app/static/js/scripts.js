function mostrarModal(id) {
    document.getElementById(id).style.display = "block";
}

function cerrarModal(id) {
    document.getElementById(id).style.display = "none";
}

document.addEventListener('DOMContentLoaded', function () {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip, {
            html: true  // Permite usar HTML dentro del tooltip
        });
    });
});
