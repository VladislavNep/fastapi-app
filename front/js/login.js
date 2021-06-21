$('#login_button').click(function() {
    let url = $(this).attr('data-url');
    let email = document.getElementById("login_email").value
    let password = document.getElementById("login_password").value

     $.ajax({
        method: 'POST',
        url: url,
        contentType: "application/json",
        data: JSON.stringify({
            email: email,
            password: password
        }),
        success: function (result) {
            let token = JSON.parse(result);
            window.localStorage.setItem('access_token', token.access_token);
            location="/users";
        },
        error: function(response){
            console.log(response);
            let alert = document.getElementById("login_error");
            alert.classList.remove('d-none');
            alert.innerHTML = response.responseText;
        }
    });
});