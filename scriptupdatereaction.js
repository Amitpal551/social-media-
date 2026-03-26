
$(document).ready(function() {
    var updateReactionCountUrl = "{% url 'update_reaction_count' %}";

    $('.reaction-button').click(function() {
        var postId = $(this).data('post-id');
        var reactionType = $(this).data('reaction-type');

        $.ajax({
            type: 'GET',
            url: updateReactionCountUrl,
            data: {
                'post_id': postId,
                'reaction_type': reactionType
            },
            success: function(data) {
                $('#likes-count').text(data.reaction_count);
                $('#dislikes-count').text(data.dislikes);
            }
        });
    });

    setInterval(function() {
        var postId = "{{ post.id }}";
        $.ajax({
            type: 'GET',
            url: updateReactionCountUrl,
            data: {
                'post_id': postId
            },
            success: function(data) {
                $('#likes-count').text(data.reaction_count);
                $('#dislikes-count').text(data.dislikes);
            }
        });
    }, 5000);
});


