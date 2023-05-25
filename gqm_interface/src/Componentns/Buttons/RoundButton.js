import React from 'react';

import style from './Button.css'

function RoundButton(props){
	return (
        <button className="RoundButton Button" onClick={props.click}>{props.text}</button>
	)
}

export default RoundButton
