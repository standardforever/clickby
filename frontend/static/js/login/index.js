import { get_environment_url } from "../config.js";

$(document).ready(function () {
    console.log(get_environment_url());
    
    // Handle form submission
    $('.submitBtn').on('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        var username = $('#username').val();
        var password = $('#password').val();
        var remember = $('input[name="remember"]').is(':checked');

        // You can add your form submission logic here (e.g., AJAX request)
        $.ajax({
            url: get_environment_url() + '/auth/token',
            method: 'POST',
            data: {
                username: username,
                password: password,
                remember: remember
            },
            success: function (response) {
                const res = JSON.parse(JSON.stringify(response))
                sessionStorage.setItem("clickbuy_access", response.access_token)
                sessionStorage.setItem("clickbuy_refresh", response.refresh_token)
                window.location.href = '/';
            },
            error: function (error) {
                console.log('Login failed', error);
            }
        });
    });
});
