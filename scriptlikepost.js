var likePostUrl = '/like-post/';
var staticUrl = '/static/';
var reactPostUrl = '/react-post/';

$(document).ready(function() {
  $('.like-button').on('click', function(e) {
    e.preventDefault();
    var post_id = $(this).val();
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var likeButton = $(this);
    var postStats = likeButton.closest('.post').find('.post-stats');

    $.ajax({
      type: 'POST',
      url: likePostUrl,
      data: {
        'post_id': post_id,
        'csrfmiddlewaretoken': csrftoken
      },
      headers: {
        'X-CSRFToken': csrftoken
      },
      success: function(data) {
        var likeCount = parseInt(postStats.find('.liked-users').text().match(/\d+/));
        if (likeButton.hasClass('liked')) {
          likeCount -= 1;
          likeButton.removeClass('liked');
        } else {
          likeCount += 1;
          likeButton.addClass('liked');
        }
        postStats.find('.liked-users').text(likeCount + ' likes');
      }
    });
});

  var post_id = $('.post').data('post-id');
    $.ajax({
      type: 'GET',
      url: '/get-reactions/',
      data: { 'post_id': post_id },
      success: function(data) {
        $.each(data.reactions, function(index, reaction) {
          var emojiSrc = '/static/image/' + reaction.emoji + '.jpg';
          $('.chosen-emoji').append('<img src="' + emojiSrc + '">');
        });
        $('.reaction-count').text(data.reaction_count);
      }
    });


    const displayedEmojis = [];
    
    $('.emoji').on('click', function(e) {
    e.preventDefault();
    var post_id = $(this).data('post-id');
    var emoji = $(this).data('emoji');
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var postStats = $(this).closest('.post').find('.post-stats');

    $.ajax({
      type: 'POST',
      url: reactPostUrl,
      data: {
        'post_id': post_id,
        'emoji': emoji,
        'csrfmiddlewaretoken': csrftoken
      },
      headers: {
        'X-CSRFToken': csrftoken
      },
      success: function(data) {
        var emojiSrc = '/static/image/' + data.emoji + '.jpg';
        if (displayedEmojis.length < 3 && !displayedEmojis.includes(data.emoji)) {
          displayedEmojis.push(data.emoji);
          postStats.find('.chosen-emoji').append('<img src="' + emojiSrc + '">');
        }
          postStats.find('.reaction-count').text(data.reaction_count);
      }
    });
  });
});
