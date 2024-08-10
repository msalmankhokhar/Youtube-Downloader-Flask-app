const themeToggleButton = document.getElementById('theme-toggle');
const themeToggleIcon = document.getElementById('theme-toggle-icon');
const headers = { Accept : 'application/json' }

themeToggleButton.addEventListener('click', async () => {
    let currentTheme = document.body.classList.toggle('theme-dark');
    if(currentTheme){ themeToggleIcon.classList.replace('fa-moon', 'fa-sun') } else { themeToggleIcon.classList.replace('fa-sun', 'fa-moon') }
    
    fetch(`/theme?value=${currentTheme}`, { headers: headers }).catch((error)=>{
        console.log(error)
    });
});