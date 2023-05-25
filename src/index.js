import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import { Route, BrowserRouter } from 'react-router-dom';
import { CookiesProvider } from "react-cookie";

import './index.css';
import Auth from './Pages/Auth/Auth'
import Goals from './Pages/Goals/Goals';
import Metrics from './Pages/Metrics/Metrics';
import Questions from './Pages/Questions/Questions';


function Router(){

    return(
        <React.StrictMode>
            <CookiesProvider>
                <BrowserRouter>
                    <Route exact path="/" component={Auth} />
                    <Route exact path="/goals" component={Goals} />
                    <Route exact path="/metrics" component={Metrics} />
                    <Route exact path="/questions" component={Questions} />
                </BrowserRouter>
            </CookiesProvider>
        </React.StrictMode>
    )
}


ReactDOM.render(<Router />, document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
