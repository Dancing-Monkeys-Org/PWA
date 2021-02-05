import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
    return (
        <div>
            <h3>Test homepage</h3>
            <small>testing</small>
            <p><Link to="/login">Go to login page</Link></p>
            <p><Link to="/about">Go to about page</Link></p>
            <p><Link to="/404">Go to 404 page</Link></p>
        </div>
    );
};

export default HomePage;
