$(function () {
    // Grab the CSRF token from the button’s data attribute
    const csrftoken = $('#connectBtn').data('csrf');

    // Tell jQuery to send it with every AJAX POST
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrftoken }
    });

    $('#connectBtn').click(function () {
        const btn = $(this);
        const username = btn.data('username');

        btn.prop('disabled', false).text('connect');

        $.post(`/user/${username}/request/`, function (data) {
            if (data.status === 'sent' || data.status === 'already_sent') {
                window.location = '/people/';   // or use {% url "people" %} if you render this JS inline
            }
        }) .fail(function () {
             // Failure → still redirect, no error shown 
              window.location = '/people/'; 
        });
    });
});




