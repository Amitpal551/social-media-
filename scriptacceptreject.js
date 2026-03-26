$(function () {
  // Accept button
  $(document).on('click', '.accept', function () {
    const btn = $(this);
    const pk = btn.data('pk');
    const csrftoken = btn.data('csrf');
    btn.prop('disabled', true).text('Accepting…');
    $.ajax({
      url: `/request/${pk}/accept/`,
      type: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      success: function (data) {
        if (data.status === 'accepted') {
          window.location.href = '/my_network/';
        }
      },
      error: function () {
        btn.text('Error').prop('disabled', false);
      }
    });
  });

  // Reject button
  $(document).on('click', '.reject', function () {
    const btn = $(this);
    const pk = btn.data('pk');
    const csrftoken = btn.data('csrf');
    btn.prop('disabled', true).text('Rejecting…');
    $.ajax({
      url: `/request/${pk}/reject/`,
      type: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      success: function (data) {
        if (data.status === 'rejected') {
          btn.closest('li').fadeOut(200, function () {
            $(this).remove();
          });
          alert('Request rejected!');
        }
      },
      error: function () {
        btn.text('Error').prop('disabled', false);
      }
    });
  });
});
