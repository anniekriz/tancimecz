document.addEventListener('DOMContentLoaded', function() {
    // Override default error message for time fields
    const timeFields = document.querySelectorAll('.vTimeField');
    timeFields.forEach(field => {
        field.addEventListener('input', function() {
            const errorElement = this.nextElementSibling;
            if (errorElement && errorElement.classList.contains('errorlist')) {
                const errorMessage = errorElement.querySelector('li');
                if (errorMessage && errorMessage.textContent.includes('Enter a valid time')) {
                    errorMessage.textContent = 'Zadejte čas ve formátu 18, 18:00 nebo 18:00:00';
                }
            }
        });
    });
});
