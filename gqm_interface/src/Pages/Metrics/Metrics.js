import React, {useState, useEffect} from 'react';
import { useCookies} from "react-cookie";

import './Metrics.css'
import {MetricsAPI} from './MetricsAPI';
import Header from "../../Componentns/Header/Header";
import MainBlock from '../../Componentns/MainBlock/MainBlock'
import RectangularButton from "../../Componentns/Buttons/RectangularButton";
import Item from "../../Componentns/Item/Item";

function Metrics(props){

    const [token, setToken, deleteToken] = useCookies(['mr-token']);
    const [metrics, setMetrics] = useState([])
    const [allMetrics, setAllMetrics] = useState([])
    const [question, setQuestion] = useState([])
    const [hasMetrics, setHasMetrics] = useState(false)
    const [isActionChoise, setIsActionChoise] = useState(true)
    const [isGenerate, setIsGenerate] = useState(false)
    const [isPrecooked, setIsPrecooked] = useState(false)
    const [isHandPick, setIsHandPick] = useState(false)
    const question_id = localStorage.getItem('question_id')
    const goal_content = localStorage.getItem('goal_content')

    useEffect(() => {
        getQuestionById()
    }, [])

    const getQuestionById = () => {
        return MetricsAPI.getQuestionById(question_id, token['mr-token'])
            .then( resp => setQuestion(resp))
    }

    const logoutUser = () => {
        deleteToken('mr-token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('goal_id');
        localStorage.removeItem('goal_content');
        localStorage.removeItem('question_id');
    }

    const goToQuestions = () => {
        localStorage.removeItem('question_id');
        window.location.href = '/questions';
    }

    const clickedGenerate = () => {
        setIsActionChoise(false)
        setIsGenerate(true)
        generateMetrics(question_id)
    }

    const generateMetrics = (question_id) => {
        return MetricsAPI.generateMetrics(question_id, token['mr-token'])
            .then( resp => setMetrics(resp.metrics))
    }

    const clickedPrecooked = () => {
        setIsActionChoise(false)
        setIsPrecooked(true)
        assignMetrics(question_id)
    }

    const assignMetrics = (question_id) => {
        return MetricsAPI.assignMetrics(question_id, token['mr-token'])
            .then( resp => setMetrics(resp.metrics))
    }

    const clickedHandPick = () => {
        setIsActionChoise(false)
        setIsHandPick(true)
        listMetrics()
    }

    const listMetrics = () => {
        return MetricsAPI.listMetrics(token['mr-token'])
            .then( resp => {
                let newList = resp.map(data => {
                    return {
                        select: false,
                        description: data.description,
                        name: data.name
                    }
                })
                setAllMetrics(newList)
            })

    }

    const saveChosenMetrics = () => {
        let newList = allMetrics.map(data => {
                    if(data.select === true) {
                        return {
                            name: data.name
                        }
                    }
                })
        var filtered = newList.filter(function (el) {
          return el != null;
        });
        return MetricsAPI.saveChosenMetrics(filtered, question_id, token['mr-token'])
            .then( resp => setMetrics(resp.metrics))
    }

    return (
        <div className="MetricsPage">
            <Header
                goBack={goToQuestions}
                goBackText={'Back to questions'}
                header={'Goal: '}
                text={goal_content}
                subheader={'Question: '}
                subtext={question.content}
                logOut={logoutUser}
            />
            <div className="MainPartContainer">
                {isActionChoise ?
                    <div className="MetricsMainBlock">
                        <h1 className="MetricsHeader">Metrics</h1>
                        <div className="TopPart">
                            {question.metrics ?
                                question.metrics.map(met => {
                                    return (
                                        <div className="Metrics">{met}</div>
                                    )
                                }) :
                                null
                            }
                        </div>
                        <div className="BottomPart">
                            <RectangularButton click={clickedGenerate} text="Generate"/>
                            <RectangularButton click={clickedPrecooked} text="Precooked"/>
                            <RectangularButton click={clickedHandPick}  text="Hand-pick"/>
                        </div>
                    </div>
                    :
                    <div className="NewMainBlock">
                        <Generate isGenerate={isGenerate} metrics={metrics} />
                        <Precooked isPrecooked={isPrecooked} metrics={metrics}/>
                        <HandPick
                            isHandPick={isHandPick}
                            metrics={allMetrics}
                            click={saveChosenMetrics}
                            setAllMetrics={setAllMetrics}
                            allMetrics={allMetrics}
                        />
                    </div>
                }
            </div>
        </div>
    )

}

function Generate(props) {
    return (
        <React.Fragment>
            {props.isGenerate ?
                <ol className="MetricsList">
                    {props.metrics.map(met => {
                        return (
                            <div>{met}</div>
                        )
                    })}
                </ol>
                : null
            }
        </React.Fragment>
    )
}

function Precooked(props) {
    return (
        <React.Fragment>
            { props.isPrecooked ?
                <ol className="MetricsList">
                    {props.metrics.map(met => {
                        return (
                            <div>{met}</div>
                        )
                    })}
                </ol>
                : null
            }
        </React.Fragment>
    )
}

function HandPick(props) {

    return (
        <React.Fragment>
            {props.metrics ?
                props.isHandPick ?
                    <form className="MetricsCheckArea">
                        <h1 className="AllMetricsHeader">Choose the appropriate metrics:</h1>
                        <ol className="ListOfAllMetrics">
                            {props.metrics.map(met => {
                                return (
                                    <li className="CheckboxContainer">
                                        <input
                                            type="checkbox"
                                            id={met.name}
                                            checked={met.select}
                                            onChange={event => {
                                                let checked = event.target.checked;
                                                props.setAllMetrics(props.allMetrics.map(data => {
                                                    if(met.name === data.name){
                                                        data.select = checked;
                                                    }
                                                    return data;
                                                }))
                                            }}
                                        />
                                        <label title={met.description} className="MetricsLabel" htmlFor={met.name}>{met.name}</label>
                                    </li>
                                )
                            })}
                        </ol>
                        <div className="ButtonContainer">
                            <RectangularButton click={props.click} text={'Save'}/>
                        </div>
                    </form>
                    : null
                :
                null
            }
        </React.Fragment>
    )
}

export default Metrics;