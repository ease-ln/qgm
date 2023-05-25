
const API_BASE = 'http://127.0.0.1:8000'

export class AuthAPI {

    static loginUser(body) {
        return fetch(`${API_BASE}/api/auth/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify( body )
        }).then( resp => resp.json())
    }

    static registerUser(body) {
        return fetch(`${API_BASE}/api/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify( body )
        }).then( resp => resp.json())
    }

}