import React from 'react';

import style from './Item.css'
import RectangularButton from '../Buttons/RectangularButton'

function Item(props){
	return (
        <div className="RowContainer">
            <li className="Item">
                <div className="Link" onClick={props.clicked}>
                    {props.content}
                </div>
                <RectangularButton click={props.delete} text={'Delete'} />
            </li>
        </div>
	)
}

export default Item
