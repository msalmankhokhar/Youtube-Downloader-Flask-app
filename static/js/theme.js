const themeToggleButton = document.getElementById('theme-toggle');
const themeToggleIcon = document.getElementById('theme-toggle-icon');
const headers = { Accept : 'application/json' }

// getting theme from localstorge and setting it
// let savedTheme = window.localStorage.getItem('darktheme')
// if (savedTheme == 'true') {
//     document.body.classList.add('theme-dark');
// }

themeToggleButton.addEventListener('click', async () => {
    let currentTheme = document.body.classList.toggle('theme-dark');
    // window.localStorage.setItem('darktheme', currentTheme);
    if(currentTheme){ themeToggleIcon.classList.replace('fa-moon', 'fa-sun') } else { themeToggleIcon.classList.replace('fa-sun', 'fa-moon') }
    
    fetch(`/theme?value=${currentTheme}`, { headers: headers }).catch((error)=>{
        console.log(error)
    });
});