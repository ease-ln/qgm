import React from 'react';

import style from './Button.css'

function RectangularButton(props){
	return (
        <button className="RectangularButton Button" onClick={props.click}>{props.text}</button>
	)
}

export default RectangularButton
