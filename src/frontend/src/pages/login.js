import React from "react";

const LoginPage = () => {
    return (
        <div>
            <ul>
                {["Alex", "John", "Fredrick", "James"].map((user, idx) => {
                    return <li key={idx}>{user}</li>
                })}
            </ul>
        </div>
    );
};

export default LoginPage;
