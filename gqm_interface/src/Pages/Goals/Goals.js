import React, {useState, useEffect} from 'react';
import { useCookies} from "react-cookie";

import './Goals.css'
import {GoalsAPI} from './GoalsAPI';
import Item from "../../Componentns/Item/Item";
import MainBlock from '../../Componentns/MainBlock/MainBlock'
import RoundButton from "../../Componentns/Buttons/RoundButton";
import RectangularButton from "../../Componentns/Buttons/RectangularButton";

function Goals(props){

    const [token, setToken, deleteToken] = useCookies(['mr-token']);
    const [goals, setGoals] = useState([])
    const [content, setContent] = useState('')
    const [isAddGoal, setIsAddGoal] = useState(false)
    const [user_id, setUserId] = useState(1)

    useEffect(() => {
        getGoals()
    }, [])

    const logoutUser = () => {
        deleteToken('mr-token');
        localStorage.removeItem('user_id');
    }

    const getGoals = () => {
        return GoalsAPI.getGoals(token['mr-token'])
            .then( resp => {
                setGoals(resp)
                let id = localStorage.getItem('user_id')
                id = Number(id)
                setUserId(id)
            })
    }

    const deleteClicked = goal => {
        GoalsAPI.deleteGoal(goal.id, token['mr-token'])
            .then( () => {
                const newGoals = goals.filter( go => go.id !== goal.id);
                setGoals(newGoals);
            })
    }

    const newGoal = goal => {
        setIsAddGoal( false)
        const newGoals = [...goals, goal];
        setGoals(newGoals);
    }

    const saveNewGoal = () => {
        console.log({content, user_id})
        GoalsAPI.createGoal({content, user_id}, token['mr-token'])
            .then( resp => newGoal(resp))
    }
    
    const goalClicked = (goal_id) => {
        localStorage.setItem('goal_id', goal_id)
        window.location.href = '/questions';
    }

    return (
        <div className="GoalsPage">
            <a className="GoalsLogOut" href="/" onClick={logoutUser}>Log out</a>
            <MainBlock>
                <h1 className="GoalsHeader">Goals</h1>
                <ol className="GoalsList">
                    {goals.length ?
                        goals.map(goal => {
                        return (
                            <Item
                                clicked={() => goalClicked(goal.id)}
                                content={goal.content}
                                delete={() => deleteClicked(goal)}
                            />
                        )
                        })
                        :
                        null
                    }
                </ol>
                {isAddGoal ?
                    <div className="NewGoalContainer">
                        <textarea className="TextNewGoal" type="text" placeholder="Enter your goal"
                            value={content} onChange={evt => setContent(evt.target.value)}/>
                        <RectangularButton click={saveNewGoal} text={'Save'}/>
                    </div>
                        : null
                }
                {isAddGoal ?
                    <div className="ButtonContainer">
                        <RoundButton click={() => setIsAddGoal(false)} text={"x"} />
                    </div>
                     :
                    <div className="ButtonContainer">
                        <RoundButton click={() => setIsAddGoal(true)} text={"+"} />
                    </div>
                }
            </MainBlock>
        </div>
    )
}

export default Goals;