import React, {useState, useEffect} from 'react';
import { useCookies} from "react-cookie";

import './Questions.css'
import {QuestionsAPI} from './QuestionsAPI';
import Item from '../../Componentns/Item/Item'
import Header from '../../Componentns/Header/Header'
import MainBlock from '../../Componentns/MainBlock/MainBlock'
import RoundButton from "../../Componentns/Buttons/RoundButton";
import RectangularButton from "../../Componentns/Buttons/RectangularButton";


function Questions(props){

    const [token, setToken, deleteToken] = useCookies(['mr-token']);
    const [questions, setQuestions] = useState([])
    const [content, setContent] = useState('')
    const [isAddQuestion, setIsAddQuestion] = useState(false)
    const [goal, setGoal] = useState([])
    const goal_id = localStorage.getItem('goal_id')


    useEffect(() => {
        getQuestions(goal_id)
        getGoalById()
    }, [])

    const logoutUser = () => {
        deleteToken('mr-token');
        localStorage.removeItem('user_id');
    }

    const getQuestions = (goal_id) => {
        return QuestionsAPI.getQuestions(goal_id, token['mr-token'])
            .then( resp => setQuestions(resp))
    }

    const deleteClicked = question => {
        QuestionsAPI.deleteQuestion(question.id, token['mr-token'])
            .then( () => {
                const newQuestions = questions.filter( qe => qe.id !== question.id);
                setQuestions(newQuestions);
            })
    }

    const newQuestion = question => {
        setIsAddQuestion( false)
        const newQuestions = [...questions, question];
        setQuestions(newQuestions);
    }

    const saveNewQuestion = () => {
        QuestionsAPI.createQuestion({content, goal_id}, token['mr-token'])
            .then( resp => newQuestion(resp))
    }

    const questionClicked = (question) => {
        localStorage.setItem('question_id', question.id)
        window.location.href = '/metrics';
    }

    const goToGoals = () => {
        localStorage.removeItem('goal_id');
        window.location.href = '/goals';
    }

    const getGoalById = () => {
        return QuestionsAPI.getGoalById(goal_id, token['mr-token'])
            .then( resp => {
                setGoal(resp)
                localStorage.setItem('goal_content', resp.content)
            })
    }

     return (
        <div className="QuestionsPage">
            <Header
                goBack={goToGoals}
                goBackText={'Back to goals'}
                header={'Goal: '}
                text={goal.content}
                logOut={logoutUser}
            />
            <div className="MainPartContainer">
                <MainBlock>
                    <h1 className="QuestionsHeader">Questions</h1>
                    <ol className="QuestionsList">
                        {questions.map(question => {
                            return (
                                <Item
                                    clicked={() => questionClicked(question)}
                                    content={question.content}
                                    delete={() => deleteClicked(question)}
                                />
                            )
                        })}
                    </ol>
                    {isAddQuestion ?
                        <div className="NewQuestionContainer">
                            <textarea className="TextNewQuestion" type="text" placeholder="Enter your question"
                                value={content} onChange={evt => setContent(evt.target.value)}/>
                            <RectangularButton click={saveNewQuestion} text={'Save'}/>
                        </div>
                        : null
                    }
                    {isAddQuestion ?
                        <div className="ButtonContainer">
                            <RoundButton click={() => setIsAddQuestion(false)} text={"x"} />
                        </div>
                         :
                        <div className="ButtonContainer">
                            <RoundButton click={() => setIsAddQuestion(true)} text={"+"} />
                        </div>
                    }
                </MainBlock>
            </div>
        </div>
    )

}

export default Questions;
