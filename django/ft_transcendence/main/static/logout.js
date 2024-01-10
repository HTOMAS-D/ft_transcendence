document.addEventListener('DOMContentLoaded', function () {
    function logoutUser() {
        console.log('logging out user...');
        fetch('/do-logout/', {
            method: 'GET',
        })
            .then(res => res.json())
            .then(data => {
                console.log('Got response', data);
                if (data.status === 'success') {
                    window.location.href = '/login';
                } else {
                    console.log("Error: ", data.errors);
                }
            })
            .catch(error => {
                console.log('Error:', error);
            });
    }

    document.getElementById('logout-user').addEventListener('click', function (event) {
        event.preventDefault();
        logoutUser();
    });
});