// Functionality for a password vision toggle. It takes the input as `id` and the div containing the icon as `show`
function passwordToggle(id, show){
    e = document.getElementById(id);
    s = document.getElementById(show);
    if (e.type == "password"){
        e.type = "text";
        s.firstChild.classList.remove('fa-eye-slash')
        s.firstChild.classList.add('fa-eye')
    }
    else{
        e.type = "password";
        s.firstChild.classList.remove('fa-eye')
        s.firstChild.classList.add('fa-eye-slash')
    }
}