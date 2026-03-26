const posts = document.querySelectorAll('.post');

Array.from(posts).reverse().forEach(post => {
  post.parentNode.appendChild(post);
});
