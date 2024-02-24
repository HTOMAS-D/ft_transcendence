function getUserInfo()
{
    return fetch("http://localhost:8082/user", {credentials: "include"}).then((res) => {
        return res.json();
    }).then((data) => {
        sessionStorage.setItem("UserInfo", JSON.stringify(data));
    });
}