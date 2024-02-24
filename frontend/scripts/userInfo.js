function getUserInfo()
{
    fetch("http://localhost:8082/user", {credentials: "include"}).then((res) => {
        console.log(res);
        return res.json();
    }).then((data) => {
        console.log("data: " + JSON.stringify(data));
        sessionStorage.setItem("UserInfo", JSON.stringify(data));
    });
}