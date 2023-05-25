import React, {useEffect, useState} from 'react';
import {useCookies} from 'react-cookie';

import {AuthAPI} from './AuthAPI';
import './Auth.css'
import MainBlock from '../../Componentns/MainBlock/MainBlock'


function Auth(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoginView, setIsLoginView] = useState(true)
    const [token, setToken] = useCookies(['mr-token']);

    useEffect( () => {
        if(token['mr-token']) window.location.href = '/goals';
    }, [token])

    const loginClicked = () => {
        AuthAPI.loginUser({username, password})
            .then( resp => {
                setToken('mr-token', resp.token)
                localStorage.setItem('user_id', resp.id)
            })
    }

    const registerClicked = () => {
        AuthAPI.registerUser({username, password})
            .then( () => loginClicked())
    }

    return (
        <div className="AuthPage">
            <MainBlock>
                {isLoginView ?
                    <h1 className="AuthHeader">LogIn</h1> :
                    <h1 className="AuthHeader">Register</h1>
                }
                <div>
                <input className="AuthInput" type="text" placeholder="username"
                           onChange={evt => setUsername(evt.target.value)}/>
                </div>
                <input className="AuthInput" type="password" placeholder="password"
                       onChange={evt => setPassword(evt.target.value)}/>
                {isLoginView ?
                    <button className="AuthButton" onClick={loginClicked}>LogIn</button> :
                    <button className="AuthButton" onClick={registerClicked}>Register</button>
                }
                {isLoginView ?
                    <a className="AuthText" onClick={() => setIsLoginView(false)}>
                        You don't have an account? Register here!
                    </a> :
                    <a className="AuthText" onClick={() => setIsLoginView(true)}>
                        You already have an account? Login here!
                    </a>
                }
            </MainBlock>
        </div>
    )
}

export default Auth;