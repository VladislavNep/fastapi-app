$('#logout_button').click(function() {
    let url = $(this).attr('data-url');
    let userToken = window.localStorage.getItem('access_token')

     $.ajax({
        method: 'POST',
        url: url,
        data: {
            email: email,
            password: password
        },
        headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            window.localStorage.removeItem('access_token')
            window.localStorage.removeItem('is_superuser')
            location="/login";
        },
        error: function(response){
            console.log(response);
        }
    });
});