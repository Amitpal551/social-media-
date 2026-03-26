


function toggleCommentForm(icon) {
  var postContainer = icon.closest('.post');
  var commentBoxContainer = postContainer.querySelector('.comment-box-container');
  var commentBox = commentBoxContainer.querySelector('.comment-box');
  if (commentBox.style.display === 'none') {
      commentBox.style.display = 'block';
      postContainer.style.marginBottom = '50px';
  } else{
    commentBox.style.display = 'none';
    postContainer.style.marginBottom = '10px';
  }
}

function submitComment(icon) {
    var postContainer = icon.closest('.post');
    var commentBoxContainer = postContainer.querySelector('.comment-box-container');
    var commentBox = commentBoxContainer.querySelector('.comment-box');
    var commentInput = commentBox.querySelector('textarea');
    var commentText = commentInput.value;
    
    // Submit comment logic here...
    commentInput.value = ''; // Clear the comment box value
    
    // Append the comment to the list of comments
    var commentsList = postContainer.querySelector('.comments-list');
    commentsList.style.display = 'block'; // Show the comments list
    
    var newComment = document.createElement('li');
    newComment.innerHTML = '<img src="{{user_profile.profileimg.url}}"> <span>{{user_profile.username}}:</span> <p>' + commentText + '</p>';
    commentsList.appendChild(newComment);
    
    // Keep the comment box visible
    commentBox.style.display = 'block';
}



  
  
  
    
  
  

  
    

$(document).ready(function() {
    event.preventDefault();
    $('.like-btn').click(function() {
        var commentId = $(this).data('comment-id');
        var postId = $(this).data('post-id');
        $.ajax({
            type: 'POST',
            url: "{% url 'like_comment' post_id comment_id %}",
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(data) {
                $('.like-btn[data-comment-id="' + commentId + '"]').text('Like (' + data.likes + ')');
            }
        });
    });

    $('.reply-btn').click(function() {
        event.preventDefault();
        var commentId = $(this).data('comment-id');
        var postId = $(this).data('post-id');
        $.ajax({
            type: 'POST',
            url: "{% url 'reply_comment' post_id comment_id %}",
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                'comment': $('#reply-textarea-' + commentId).val()
            },
            success: function(data) {
                $('#reply-textarea-' + commentId).val('');
                $('#replies-list-' + commentId).append('<li>' + data.reply + ' by ' + data.user + '</li>');
            }
        });
    });
})
