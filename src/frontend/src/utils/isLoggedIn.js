import React from 'react';

const isLoggedIn = () => {
    const loginVal = JSON.parse(localStorage.getItem("login"));
    let status = false;
    if (loginVal !== null) {
        status = loginVal.login ?? false;
    }
    return status;
}

export default isLoggedIn;
