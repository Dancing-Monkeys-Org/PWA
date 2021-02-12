import React from 'react';

const isAuthenticated = (userName, password) => {
    try {
        return fetch("https://dancingmonkeys.tech/api/login", {
            method: "POST",
            body: JSON.stringify({ "username": userName, "password": password }),
            headers: {
                "Content-Type": "application/json",
                "Accept": "*/*"
            }
        })
        .then(res => {
            return res.status === 200 ? res.json() : null;
        })
        .then(data => {
            try {
                localStorage.setItem("login", JSON.stringify({
                    login: true,
                    token: data.access_token
                }));
            } catch {
                localStorage.setItem("login", JSON.stringify({
                    login: false,
                }));
            }
        });
    } catch(ex) {
        localStorage.setItem("login", JSON.stringify({
            login: false,
        }));
    }
};

export default isAuthenticated;
