const API_BASE = 'http://127.0.0.1:8000'

export class QuestionsAPI {

    static getQuestions (goal_id, token) {
        return fetch(`${API_BASE}/api/goal/questions/${goal_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        }).then( resp => resp.json())
    }

    static deleteQuestion (question_id, token) {
        return fetch(`${API_BASE}/api/questions/${question_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
    }

    static createQuestion (body, token) {
        return fetch(`${API_BASE}/api/questions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify( body )
        }).then( resp => resp.json())
    }

    static getGoalById (goal_id, token) {
        return fetch(`${API_BASE}/api/goals/${goal_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        }).then( resp => resp.json())
    }

}