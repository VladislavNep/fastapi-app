$('#singup_button').click(function() {
    let url = $(this).attr('data-url');
    let email = document.getElementById("reg_email").value
    let firstname = document.getElementById("reg_firstname").value
    let lastname = document.getElementById("reg_lastname").value
    let password = document.getElementById("reg_password").value

     $.ajax({
        method: 'POST',
        url: url,
        contentType: "application/json",
        data: JSON.stringify({
            email: email,
            first_name: firstname,
            last_name: lastname,
            password: password
        }),
        success: function (result) {
            let payload = JSON.parse(result);
            window.localStorage.setItem('access_token', payload.access_token);
            window.localStorage.setItem('is_superuser', payload.is_superuser);
            location="/users";
        },
        error: function(response){
            console.log(response);
            let alert = document.getElementById("reg_error");
            alert.classList.remove('d-none');
            alert.innerHTML = response.responseText;
        }
    });
});