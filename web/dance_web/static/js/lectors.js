document.addEventListener('DOMContentLoaded', function () {
    const lectorsContainer = document.createElement('div');
    lectorsContainer.id = 'lectors-container';
    
    // Find the initial lector field
    const firstLectorField = document.querySelector('select[name="lector"]');

    if (firstLectorField) {
        // Create add button
        const addLectorButton = document.createElement('button');
        addLectorButton.textContent = '+';
        addLectorButton.type = 'button';
        addLectorButton.classList.add('add-lector');
        
        // Create a container for the first lector field and add button
        const firstLectorContainer = document.createElement('div');
        firstLectorContainer.appendChild(firstLectorField.cloneNode(true));
        firstLectorContainer.appendChild(addLectorButton);
        
        // Append the container to lectorsContainer
        lectorsContainer.appendChild(firstLectorContainer);

        // Insert the lectorsContainer after the initial lector field's parent element
        firstLectorField.parentNode.insertBefore(lectorsContainer, firstLectorField.nextSibling);

        // Remove the initial lector field to avoid duplication
        firstLectorField.remove();

        addLectorButton.addEventListener('click', function () {
            const newLectorField = firstLectorField.cloneNode(true);
            newLectorField.value = '';
            const removeButton = document.createElement('button');
            removeButton.textContent = '-';
            removeButton.type = 'button';
            removeButton.classList.add('remove-lector');

            const fieldContainer = document.createElement('div');
            fieldContainer.appendChild(newLectorField);
            fieldContainer.appendChild(removeButton);
            lectorsContainer.appendChild(fieldContainer);

            removeButton.addEventListener('click', function () {
                lectorsContainer.removeChild(fieldContainer);
            });
        });
    } else {
        console.error('Lector field not found');
    }
});
