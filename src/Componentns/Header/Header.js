import React from 'react';

import style from './Header.css'

function Header(props){
	return (
        <div className="HeaderContainer">
            <a className="Navigation" onClick={props.goBack}><span>{props.goBackText}</span></a>
            <div className="HeaderTextContainer">
                <h1 className="HeaderText"><b>{props.header}</b> {props.text}</h1>
                <h2 className="HeaderText"><b>{props.subheader}</b> {props.subtext}</h2>
            </div>
            <a className="Navigation" href="/" onClick={props.logOut}><span>Log out</span></a>
        </div>
	)
}

export default Header
