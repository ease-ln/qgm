const API_BASE = 'http://127.0.0.1:8000'

export class GoalsAPI {

    static getGoals (token) {
        return fetch(`${API_BASE}/api/user/goals/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        }).then( resp => resp.json())
    }

    static deleteGoal (goal_id, token) {
        return fetch(`${API_BASE}/api/goals/${goal_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
    }

    static createGoal (body, token) {
        return fetch(`${API_BASE}/api/goals/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify( body )
        }).then( resp => resp.json())
    }

}