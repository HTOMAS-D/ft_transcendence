function showPage(page){
    document.querySelectorAll('form').forEach(div => {
        div.style.display = 'none';
    })
    document.querySelector(`#${page}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('button').forEach(button =>{
        button.onclick = function(){
            showPage(this.dataset.page)
        }
    });
})

document.addEventListener('DOMContentLoaded', function(){
    function submitUserForm(){
        console.log('submitting user form...');
        const form = document.getElementById('register-form');
        const errorContainer = document.getElementById('error-container');

        fetch('/register/', {
            method: 'POST',
            body: new FormData(form),
        })
        .then(res => res.json())
        .then(data =>{
            console.log('Got response', data);
            if (data.status === 'success'){
                form.reset();
                errorContainer.innerHTML = '';
                window.location.href='/login'
            } else {
                console.log("errors found in the form", data.errors);
                errorContainer.innerHTML = data.errors.join('<br>');
            }
        })
        .catch(error =>{
            console.log('Error:', error);
        })
    }

    function submitLogin(){
        console.log('loggin in the user');
        const form = document.getElementById('login-form');
        const loginErrorContainer = document.getElementById('login-error-container');

        fetch('/do-login/', {
            method: 'POST',
            body: new FormData(form),
        })
        .then(res => res.json())
        .then(data =>{
            console.log('got response', data);
            loginErrorContainer.innerHTML = '';
            if(data.status === 'success'){
                form.reset();
                window.location.href = '/'
            } else {
                console.log('Errors ocurred during login', data.errors)
                loginErrorContainer.innerHTML = data.errors.join('<br>');
            }

        })
        .catch(error => {
            console.log('Error: ', error);
            loginErrorContainer.innerHTML = 'Invalid Credentials';
        })
    }

    document.getElementById('register-user').addEventListener('click', function (event){
        event.preventDefault();
        submitUserForm();
    });

    document.getElementById('login-user').addEventListener('click', function(event){
        event.preventDefault();
        submitLogin();
    });
})
