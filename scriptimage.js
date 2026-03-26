const fileinput = document.getElementById('file-input');
const botton = document.getElementById('botton');
const fileNameElement = document.getElementById('.file-name');


botton.addEventListener('click',()=>{
    fileinput.click();
});

fileinput.addEventListener('change',()=>{
    const selectedFile = fileinput.files[0];
    fileNameElement.textContent = selectedFile.name;
});




function confirmDelete(event) {
  if (confirm("Are you sure you want to delete this item?")) {
    // User clicked OK, submit the form
    document.getElementById("delete-form").submit();
    return true;
  } else {
    // User clicked Cancel, prevent default action
    return false;
  }
}
