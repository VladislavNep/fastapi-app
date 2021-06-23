$(document).ready(function () {
    let userToken = window.localStorage.getItem('access_token');
    let is_superuser = window.localStorage.getItem('is_superuser');

     $.ajax({
        method: 'GET',
        url: '/api/v1/users',
        data: {},
        headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            let user_data
            result.forEach(function(data, index) {
              user_data += `
                <tr id="row_${data.id}">
                  <th scope="row">${data.id}</th>
                  <td id="email">${data.email}</td>
                  <td id="first_name">${data.first_name}</td>
                  <td id="last_name">${data.last_name}</td>
                  <td id="is_superuser">${data.is_superuser}</td>
                  <td class="d-flex justify-content-end">
                  <button type="button" class="btn btn-warning mx-3" data-bs-toggle="modal" data-bs-target="#userUpdate"
                  data-url="/api/v1/users/${data.id}/update" data-id="${data.id}" id="userUpdateButton">Обновить</button>
                  <button type="button" class="btn btn-danger" id="userDeleteButton" data-url="/api/v1/users/${data.id}/delete">Удалить</button>
                  </td>
                </tr>
                `
            });
            $("#user_list").html(user_data);
            setActionButtons(is_superuser);
        },
        error: function(response){
            console.log(response);
            if (response.status === 401){
                window.localStorage.removeItem('access_token');
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }

        }
    });
})


$(document).on("click", '#userDeleteButton',function() {
    console.log(true)
    let userToken = window.localStorage.getItem('access_token')
    let url = $(this).attr('data-url');

     $.ajax({
        method: 'DELETE',
        url: url,
        data: {},
         headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            location="/users";
        },
        error: function(response){
            if (response.status === 401){
                window.localStorage.removeItem('access_token')
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }
            console.log(response);
        }
    });
});



$('#user_add_button').click(function() {
    let userToken = window.localStorage.getItem('access_token')
    let url = $(this).attr('data-url');
    let email = document.getElementById("add_email").value
    let password = document.getElementById("add_password").value
    let firstname = document.getElementById("add_first_name").value
    let lastname = document.getElementById("add_last_name").value
    let is_superuser = document.querySelector('#flexSwitchCheckAdd').checked

     $.ajax({
        method: 'POST',
        url: url,
        contentType: "application/json",
        data: JSON.stringify({
            email: email,
            first_name: firstname,
            last_name: lastname,
            password: password,
            is_superuser: is_superuser,
            is_active: true,
        }),
         headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            clearInputs();
            location="/users";
        },
        error: function(response){
            if (response.status === 401){
                window.localStorage.removeItem('access_token')
                clearInputs();
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                clearInputs();
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }
            console.log(response);
        }
    });
});


let userUpdateModal = document.getElementById('userUpdate')
userUpdateModal.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget
    let url = button.getAttribute('data-url')
    let id = button.getAttribute('data-id')
    let buttonModel = userUpdateModal.querySelector('#update_user_button')
    buttonModel.setAttribute('data-url', url)
    setDefaultValue(id, userUpdateModal)
})

$(document).on("click", '#update_user_button', function() {
    let userToken = window.localStorage.getItem('access_token')
    console.log(userToken)
    let url = $(this).attr('data-url');
    let email = document.getElementById("update_email").value
    let password = document.getElementById("update_password").value
    let firstname = document.getElementById("update_first_name").value
    let lastname = document.getElementById("update_last_name").value
    let is_superuser = document.querySelector('#flexSwitchCheckUpdate').checked

     $.ajax({
        method: "PUT",
        url: url,
        contentType: "application/json",
        data: JSON.stringify({
            email: email,
            first_name: firstname,
            last_name: lastname,
            password: password,
            is_superuser: is_superuser,
        }),
         headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            clearInputs();
            location="/users";
        },
        error: function(response){
            console.log(true);
            if (response.status === 401){
                window.localStorage.removeItem('access_token');
                clearInputs();
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                clearInputs();
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }
            console.log(response);
        }
    });
});

function clearInputs(){
    let inputs = document.querySelectorAll('input');

    for (let i = 0;  i < inputs.length; i++) {
      inputs[i].value = '';
    }
}


$(document).on("click", '#logout', function() {
    let userToken = window.localStorage.getItem('access_token')
    let url = $(this).attr('data-url');

     $.ajax({
        method: "POST",
        url: url,
        contentType: "application/json",
        data: {},
         headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            window.localStorage.removeItem('access_token');
            location="/login";
        },
        error: function(response){
            console.log(true);
            if (response.status === 401){
                window.localStorage.removeItem('access_token');
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }
            console.log(response);
        }
    });
});

$(document).on("click", '#sources', function (){
    let userToken = window.localStorage.getItem('access_token');

     $.ajax({
        method: 'GET',
        url: '/api/v1/sources',
        data: {},
        headers: {
            Authorization: `Bearer ${userToken}`
        },
        success: function (result) {
            let user_data
            result.forEach(function(data, index) {
              user_data += `
                <tr>
                  <th scope="row">${data.id}</th>
                  <td>${data.name}</td>
                </tr>
                `
            });
            $("#sources_list").html(user_data);
        },
        error: function(response){
            console.log(response);
            if (response.status === 401){
                window.localStorage.removeItem('access_token');
                location="/login";
            } else {
                let alert = document.getElementById("alert_error");
                alert.classList.remove('d-none');
                alert.innerHTML = response.responseText;
            }

        }
    });
})

function setActionButtons(is_superuser) {
    if (is_superuser === "false"){
        let userAddButton = document.getElementById('userAddButton');
        const userDeleteButton = document.querySelectorAll('#userUpdateButton');
        const userUpdateButton = document.querySelectorAll('#userDeleteButton');
        userAddButton.classList.add("disabled")
        for (let elem of userDeleteButton) {
          elem.classList.add("disabled")
        }
        for (let elem of userUpdateButton) {
          elem.classList.add("disabled")
        }

    }

}

function setDefaultValue(id, modal){
    let row_data = document.getElementById(`row_${id}`)

    modal.querySelector("#update_email").value = row_data.querySelector("#email").textContent;
    modal.querySelector("#update_first_name").value = row_data.querySelector("#first_name").textContent;
    modal.querySelector("#update_last_name").value = row_data.querySelector("#last_name").textContent;
    const is_superuser = row_data.querySelector("#is_superuser").textContent
    if (is_superuser === 'true'){
        modal.querySelector('#flexSwitchCheckUpdate').checked = true;
    } else {
        modal.querySelector('#flexSwitchCheckUpdate').checked = false;
    }

}