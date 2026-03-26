document.getElementById('add-education-btn').addEventListener('click', function() {
  document.getElementById('education-popup').style.display = 'block';
  document.getElementById('education-section').scrollIntoView();

  
});

document.querySelector('.close').addEventListener('click', function() {
  document.getElementById('education-popup').style.display = 'none';
});
