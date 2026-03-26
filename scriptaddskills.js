document.getElementById('add-skill-btn').addEventListener('click', function() {
  document.getElementById('skill-popup').style.display = 'block';
  document.getElementById('skill-section').scrollIntoView();

  
});

document.querySelector('.close').addEventListener('click', function() {
  document.getElementById('skill-popup').style.display = 'none';
});



document.getElementById('add-language-btn').addEventListener('click', function() {
  document.getElementById('language-popup').style.display = 'block';
  document.getElementById('language-section').scrollIntoView();

  
});

document.querySelector('.close').addEventListener('click', function() {
  document.getElementById('language-popup').style.display = 'none';
});



// Show the popup when the "Add / Edit About" button is clicked
document.getElementById('add-about-btn').addEventListener('click', function () {
    document.getElementById('about-popup').style.display = 'block';
});

// Hide the popup when the close image is clicked
document.querySelector('.popup .close').addEventListener('click', function () {
    document.getElementById('about-popup').style.display = 'none';
});

// If the URL contains #about-section, scroll to it (useful after redirect)
if (window.location.hash === '#about-section') {
    setTimeout(function () {
        var el = document.getElementById('about-section');
        if (el) el.scrollIntoView();
    }, 100);
}



document.addEventListener('click', function (e) {
    if (e.target.classList.contains('read-more')) {
        e.preventDefault();
        const container = e.target.closest('.about-text');
        container.querySelector('.short').style.display = 'none';
        container.querySelector('.full').style.display = 'inline';
        e.target.style.display = 'none';
    }
});