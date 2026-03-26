document.getElementById('add-experience-btn').addEventListener('click', function() {
  document.getElementById('experience-popup').style.display = 'block';
  document.getElementById('experience-section').scrollIntoView();
});

var closeButtons = document.querySelectorAll('.close');
closeButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    this.parentElement.parentElement.style.display = 'none';
  });
});
