function passwordValidation(password)
{
    if (password.length < 8)
        return false;
    if (!/\d/.test(password)) // Check for digit using regex
        return false
    if (!/[A-Z]/.test(password)) // Check for capital letter
        return false

    // Check if it contains any special characters
    special_chars = " !\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"
    if(!Array.from(special_chars).some((c) => password.includes(c)))
        return false;
    // Check if it only contains the following characters
    if (!/^[a-zA-Z0-9 !"#$%&'()*+,./:;<=>?@\[\]^_`{\|}~\-]+$/.test(password))
        return false
    return true
}

function usernameValidation(username)
{
    return /^([A-Z]|[a-z]|_|-|[1-9])+$/.test(username) && username.length >= 3
}

function totpKeyValidation(key)
{
    return /^([0-9]){6}$/.test(key)
}