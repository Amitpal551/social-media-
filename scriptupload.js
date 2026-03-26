
const ImageInput = document.getElementById('image-input');
const VideoInput = document.getElementById('video-input');
const EventInput = document.getElementById('event-input');
const postButton = document.querySelector('button[type="submit"]');

imageInput.addEventListener('change', () => {
    document.getElementById('post-type').value = 'image';
});
  
videoInput.addEventListener('change', () => {
    document.getElementById('post-type').value = 'video';
});
  
eventInput.addEventListener('change', () => {
    document.getElementById('post-type').value = 'event';
});
  


postButton.addEventListener('submit',(e)=>{
    e.preventDefault();
    const formData = new FormData();
    formData.append('caption', document.querySelector('textarea').value);
    formData.append('post_type', document.getElementById('post-type').value);

    if
    (ImageInput.files.length > 0){
        formData.append('image', ImageInput.files[0]);
    }
    if
    (VideoInput.files.length > 0){
        formData.append('video', VideoInput.files[0]);
    }
    if
    (EventInput.files.length > 0){
        formData.append('event', EventInput.files[0]);
    }
    fetch( "{% url 'create_post' %}",{
        method:'POST',
        body:formData,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        
    })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.error(error));
    
});



