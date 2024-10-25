document.addEventListener('DOMContentLoaded', function () {
    const firstNameInput = document.querySelector('input[name=firstName]');
    const lastNameInput = document.querySelector('input[name=lastName]');
    const slugInput = document.querySelector('input[name=slug]');

    if (firstNameInput && lastNameInput && slugInput) {
        const charMap = {
            'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i', 'ň': 'n',
            'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
            'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I', 'Ň': 'N',
            'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'
        };

        const slugify = (val) => {
            return val.toString().toLowerCase().trim()
                .replace(/[áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]/g, (match) => charMap[match])
                .replace(/[\s\W-]+/g, '-');
        };

        const updateSlug = () => {
            const fullName = `${firstNameInput.value} ${lastNameInput.value}`;
            slugInput.setAttribute('value', slugify(fullName));
        };

        firstNameInput.addEventListener('input', updateSlug);
        lastNameInput.addEventListener('input', updateSlug);
    }
});
