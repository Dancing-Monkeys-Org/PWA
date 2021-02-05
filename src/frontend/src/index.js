import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
// Pages
import HomePage from "./pages";
import NotFoundPage from "./pages/404";
import LoginPage from "./pages/login";
import AboutPage from "./pages/about";

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Switch>
      <Route exact path="/" component={HomePage} />
      <Route exact path="/404" component={NotFoundPage} />
      <Route exact path="/login" component={LoginPage} />
      <Route exact path="/about" component={AboutPage} />
      <Redirect to="/404" />
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
