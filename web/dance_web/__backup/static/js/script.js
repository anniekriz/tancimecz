document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.toggle-description');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const description = this.previousElementSibling;
            if (description.style.height === '40px' || !description.style.height) {
                description.style.height = description.scrollHeight + 'px';
                this.textContent = '↑';
            } else {
                description.style.height = '40px';
                this.textContent = '↓';
            }
        });
    });
});
