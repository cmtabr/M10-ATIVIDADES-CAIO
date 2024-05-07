import http from 'k6/http';
import { check, sleep } from 'k6';
import { URLSearchParams } from 'https://jslib.k6.io/url/1.0.0/index.js';

export let options = {
    stages: [
        { duration: '10s', target: 100 },
        { duration: '10s', target: 10 },
        { duration: '10s', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<250'],
    }
};

const BASE_URL = 'http://backend:5000';
const USERNAME = 'teste';
const PASSWORD = 'teste123';

function generateRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}

export default function () {
    const loginParams = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const searchParams = new URLSearchParams([
        ['username', USERNAME],
        ['password', PASSWORD],
    ]);

    let params = {
        headers: {
            "Content-Type": "application/json",
            "x-key": "token",
            "x-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjF9.USgVde3Co83AeNIedm_qmqAkDij5nEYNz5ZYPBL84BU",
        },
    };

    const loginRes = http.post(`${BASE_URL}/api/login?${searchParams.toString()}`, loginParams);

    check(loginRes, {
        'logged in successfully': (resp) => resp.status === 200,
        'auth token received': (resp) => resp.json()['access token'] !== null || undefined,
    });

    // Create a Todo
    let createTodoBody = {
        "id": 1,
        "task": "Test",
        "description": 'Test',
        "status": 2,
        "priority": 2,
    }; 

    const createRes = http.post(`${BASE_URL}/api/create_todo`, JSON.stringify(createTodoBody), params);

    check(createRes, {
        'created todo successfully': (resp) => resp.json('message') === 'Todo created successfully',
    });

    //Fetch Todos
    let todosRes = http.get(`${BASE_URL}/api/todos`, params);
    check(todosRes, {
        'retrieved todos successfully': (resp) => resp.status === 200,
    });

    // Update a Todo
    let updateTodoParams = {
        "id": generateRandomInt(1, 1000),
        "task": "Jeito certo de fazer",
        "description": 'Test',
        "status": 2,
        "priority": 2,
    };

    let updateRes = http.put(`${BASE_URL}/api/update`, JSON.stringify(updateTodoParams), params);

    check(updateRes, {
        'updated todo successfully': (resp) => resp.json('message') === 'Todo updated successfully',
    });

    // Delete a Todo
    let deleteParams = {
        "id": generateRandomInt(1, 1000),
        "task": "Jeito certo de fazer",
        "description": 'Test',
        "status": 2,
        "priority": 2,
    }

    let deleteRes = http.del(`${BASE_URL}/api/delete`, JSON.stringify(deleteParams), params);
    check(deleteRes, {
        'deleted todo successfully': (resp) => resp.json('message') === 'Todo deleted successfully',
    });

    sleep(1); // Timer para não sobrecarregar o servidor
}
