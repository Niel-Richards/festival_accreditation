function goBack() {
    const backButton = document.getElementById('backBtn')
    backButton.addEventListener('click', () => {
        window.history.back();
    });
}

document.addEventListener('DOMContentLoaded', goBack)