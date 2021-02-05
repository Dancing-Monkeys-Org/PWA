import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
    return (
        <div>
            <h3>Test homepage</h3>
            <small>testing</small>
            <p><Link to="/test">Go to test page</Link></p>
            <p><Link to="/404">Go to 404 page</Link></p>
        </div>
    );
};

export default HomePage;
