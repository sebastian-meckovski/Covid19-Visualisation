 alert('If you see this alert, then your custom JavaScript script has run!')

 var toggleButton = document.getElementsByClassName('toggle-button')[0]
 var navBarLinks = document.getElementsByClassName('navbar-links')[0]

 function toggleFunction() {
     navBarLinks.classList.toggle('active')
 }

 toggleButton.addEventListener('click', toggleFunction)