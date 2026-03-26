
const shareButtons = document.querySelectorAll('.share-btn');

shareButtons.forEach((shareButton) => {
  const shareLinksContainer = shareButton.parentNode.querySelector('.share-links');
  let isShareLinksOpen = false;

  shareButton.addEventListener('click', () => {
    if (isShareLinksOpen) {
      shareLinksContainer.style.display = 'none';
      isShareLinksOpen = false;
    } else {
      shareLinksContainer.style.display = 'block';
      isShareLinksOpen = true;
    }
  });

  document.addEventListener('click', (e) => {
    if (!shareButton.contains(e.target) && !shareLinksContainer.contains(e.target)) {
      shareLinksContainer.style.display = 'none';
      isShareLinksOpen = false;
    }
  });

  const shareLinks = shareLinksContainer.querySelectorAll('a');

  shareLinks.forEach((shareLink) => {
    shareLink.addEventListener('click', (event) => {
      event.preventDefault();
      const postUrl = window.location.href;
      const postId = postUrl.split('/').pop();
      if (shareLink.classList.contains('facebook-share')) {
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(postUrl)}&title=${encodeURIComponent(document.title)}&quote=${encodeURIComponent(document.querySelector('.post-author small').textContent)}`, '_blank', 'width=600,height=400');
      } else if (shareLink.classList.contains('whatsapp-share')) {
        window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(`Check out this post: ${postUrl}`)}`, '_blank', 'width=600,height=400');
      } else if (shareLink.classList.contains('linkedin-share')) {
        window.open(`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(postUrl)}&title=${encodeURIComponent(document.title)}&summary=${encodeURIComponent(document.querySelector('.post-author small').textContent)}`, '_blank', 'width=600,height=400');
      } else if (shareLink.classList.contains('twitter-share')) {
        window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(postUrl)}&text=${encodeURIComponent(`Check out this post: ${postUrl}`)}&via=${encodeURIComponent('YourTwitterHandle')}`, '_blank', 'width=600,height=400');
      }

      // Redirect to post page
      // window.location.href = `/post/${postId}`;
    });
  });
});


