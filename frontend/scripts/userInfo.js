function setUserInfo(body) {
    sessionStorage.setItem("UserInfo", body);
    const event = new CustomEvent("UserInfoUpdate");
    window.dispatchEvent(event);
}

function getUserInfo()
{
    return fetch("http://localhost:8082/user", {credentials: "include"}).then((res) => {
        return res.json();
    }).then((data) => {
        setUserInfo(JSON.stringify(data));
    });
}