const imagePostBtn = document.querySelector('.image-post-btn');
const dropdownMenu = document.querySelector('.dropdown-menu');
const imageFileinput = document.querySelector('#image-file');
const postBtn = document.querySelector('.post-btn');


imagePostBtn.addEventListener('click',()=>{
    dropdownMenu.computedStyleMap.display = 'block';
});

postBtn.addEventListener('click',()=>{
    const imageFile = imageFileinput.files[0];
    const formData = new FormData();
    formData.append('image',imageFile);

    fetch('/post-image/',{
        method:'POST',
        body:formData,
    })
    .then((response)=>response.json())
    .then((data)=>{
        console.log(data);
        //Display posted iamge
        const postedimage = document.createElement('img');
        postedimage.src = data.image;
        document.body.appendChild(postedimage);
    })
    .catch((error) => console.error(error));
});
