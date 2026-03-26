   

   
    const showAllEducationBtn = document.querySelector('.show-all-education-btn');

  
    if (showAllEducationBtn) {
      showAllEducationBtn.addEventListener('click', () => {
        const remainingEducationList = document.getElementById('remaining-education-list');
        if (remainingEducationList.style.display === 'block') {
          remainingEducationList.style.display = 'none';
          showAllEducationBtn.textContent = 'Show all Education';
        } else {
          remainingEducationList.style.display = 'block';
          showAllEducationBtn.textContent = 'Hide Education';
        }
      });
    } else {
      console.error("Button not found");
    }
  
   



   const showAllExperienceBtn = document.getElementById('show-all-experience-link');
const remainingExperienceList = document.getElementById('remaining-experience-list');

showAllExperienceBtn.addEventListener('click', () => {
if (remainingExperienceList.style.display === 'block') {
remainingExperienceList.style.display = 'none';
showAllExperienceBtn.textContent = 'Show all Experience';
} else {
remainingExperienceList.style.display = 'block';
showAllExperienceBtn.textContent = 'Hide Experience';
}
});
  

const showAllSkillBtn = document.getElementById('show-all-skill-link');
const remainingSkillList = document.getElementById('remaining-skill-list');

showAllSkillBtn.addEventListener('click', () => {
if (remainingSkillList.style.display === 'block') {
remainingSkillList.style.display = 'none';
showAllSkillBtn.textContent = 'Show all Skills';
} else {
remainingSkillList.style.display = 'block';
showAllSkillBtn.textContent = 'Hide Skills';
}
});
  
  


