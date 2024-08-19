$(document).ready(function() {
    $('#submitbtn').on('click', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get values from input fields
        const username = $('#username').val();
        const password = $('#password').val();

        // Send a POST request to the /check_user endpoint using jQuery
        $.ajax({
            url: 'http://localhost:8000/check_user/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(data) {
                // Handle successful authentication
                if (data.status === 'success') {
                    // Store user details in localStorage
                    localStorage.setItem('userid', data.user._id);
                    localStorage.setItem('username', data.user.username);
                    // Redirect to dashboard.html
                    window.location.href = './dashboard.html';
                } else {
                    showErrorCard('Login failed: ' + data.message);
                }
            },
            error: function(jqXHR) {
                // Handle errors
                const response = jqXHR.responseJSON;
                const message = response.detail ? response.detail[0].msg : 'An error occurred';
                showErrorCard('Error: ' + message);
            }
        });
    });

    // Function to display the error card
    function showErrorCard(message) {
        // Create the error card
        const errorCard = `
            <div id="errorCard" class="uk-card uk-card-primary uk-card-hover uk-card-body uk-light" style="background-color: red; color: white; position: fixed; top: 0; width: 100%; z-index: 9999;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 class="uk-card-title">Error</h3>
                    <button id="closeErrorCard" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer;">&times;</button>
                </div>
                <p>${message}</p>
            </div>
        `;

        // Append the error card to the body
        $('body').prepend(errorCard);

        // Attach click event to close button
        $('#closeErrorCard').on('click', function() {
            $('#errorCard').remove();
        });
    }
});
