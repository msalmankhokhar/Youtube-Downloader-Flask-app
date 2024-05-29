const themeToggleButton = document.getElementById('theme-toggle');

document.body.onload = (event)=>{
    let savedTheme = window.localStorage.getItem('darktheme')
    if (savedTheme == 'true') {
        document.body.classList.add('theme-dark');
    }
}

themeToggleButton.addEventListener('click', () => {
    let currentTheme = document.body.classList.toggle('theme-dark');
    window.localStorage.setItem('darktheme', currentTheme);
});