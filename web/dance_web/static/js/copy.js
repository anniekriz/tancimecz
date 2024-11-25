document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".copy-button").forEach((button) => {
        button.addEventListener("click", (event) => {
            const rowData = event.target.closest("tr").innerText;
            navigator.clipboard.writeText(rowData).then(() => {
                alert("Copied: " + rowData);
            });
        });
    });
});
