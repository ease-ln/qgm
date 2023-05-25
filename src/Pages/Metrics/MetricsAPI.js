const API_BASE = 'http://127.0.0.1:8000'

export class MetricsAPI {

    static getQuestionById (question_id, token) {
        return fetch(`${API_BASE}/api/questions/${question_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        }).then( resp => resp.json())
    }

    static generateMetrics (question_id, token) {
        return fetch(`${API_BASE}/api/question/generate-metrics/${question_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        }).then( resp => resp.json())
    }

    static assignMetrics (question_id, token) {
        return fetch(`${API_BASE}/api/question/assign-metrics/${question_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        }).then( resp => resp.json())
    }

    static listMetrics (token) {
        return fetch(`${API_BASE}/api/metrics/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        }).then( resp => resp.json())
    }

    static saveChosenMetrics (metrics, question_id, token) {
        return fetch(`${API_BASE}/api/question/save-metrics/${question_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify( metrics )
        }).then( resp => resp.json())
    }

}