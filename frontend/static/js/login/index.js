import { get_environment_url } from "../config.js";

$(document).ready(function () {
    const dynamic_url = get_environment_url();
    
    // Handle form submission
    $('.submitBtn').on('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        var username = $('#username').val();
        var password = $('#password').val();
        var remember = $('input[name="remember"]').is(':checked');

        // You can add your form submission logic here (e.g., AJAX request)
        $.ajax({
            url: dynamic_url.api_url + '/auth/token',
            method: 'POST',
            data: {
                username: username,
                password: password,
                remember: remember
            },
            success: function (response) {
                const res = JSON.parse(JSON.stringify(response));
                localStorage.setItem("clickbuy_access", response.access_token);
                localStorage.setItem("clickbuy_refresh", response.refresh_token);
                window.location.href = '/';
            },
            error: function (xhr, status, error) {
                console.log('Login failed', xhr.responseJSON);
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    $('#error-message').text('Login failed: ' + xhr.responseJSON.detail).show();
                } else {
                    $('#error-message').text('Login failed: ' + error).show();
                }
            }
        });
    });
});
