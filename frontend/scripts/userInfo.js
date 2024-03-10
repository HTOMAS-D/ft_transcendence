function setUserInfo(body) {
    sessionStorage.setItem("UserInfo", body);
    const event = new CustomEvent("UserInfoUpdate");
    window.dispatchEvent(event);
}

function getUserInfo()
{
    return fetch("/api/user/", {credentials: "include"}).then((res) => {
        if (res.ok)
            return res.json();
        else
            return Promise.reject("response error");
    }).then((data) => {
        setUserInfo(JSON.stringify(data));
    });
}