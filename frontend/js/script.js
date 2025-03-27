// Configuration
const API_BASE_URL = 'http://localhost:8000';
let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');
let firstQuestionId = null;
let currentQuestionId = localStorage.getItem('currentQuestionId') ? parseInt(localStorage.getItem('currentQuestionId')) : null;

// Page-specific initialization
if (document.getElementById('quizPrompt')) { // Index page
    window.onload = async () => {
        if (!await checkAuth()) return;
        await checkUnfinishedQuiz();
        await loadPopularTopics();
    };
} else if (document.getElementById('questionText')) { // Quiz page
    window.onload = async () => {
        if (!await checkAuth()) return;
        await loadQuestion();
    };
}

// Authentication check with token refresh
async function checkAuth() {
    if (!accessToken || !refreshToken) {
        window.location.href = '/login.html';
        return false;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/user/check-auth/`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) {
            if (response.status === 401) {
                const refreshed = await refreshAccessToken();
                if (!refreshed) {
                    logout();
                    return false;
                }
                // Retry the original request with new access token
                const retryResponse = await fetch(`${API_BASE_URL}/user/check-auth/`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });
                if (!retryResponse.ok) {
                    logout();
                    return false;
                }
            } else {
                logout();
                return false;
            }
        }
        return true;
    } catch (error) {
        console.error('Auth check failed:', error);
        logout();
        return false;
    }
}

// Refresh access token
async function refreshAccessToken() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });
        if (!response.ok) {
            return false;
        }
        const data = await response.json();
        accessToken = data.access;
        localStorage.setItem('accessToken', accessToken);
        return true;
    } catch (error) {
        console.error('Token refresh failed:', error);
        return false;
    }
}

// Logout helper
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('currentQuestionId');
    window.location.href = '/login.html';
}

// Login function with JWT tokens
async function login() {
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;
    try {
        const response = await fetch(`${API_BASE_URL}/api/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (data.access && data.refresh) {
            accessToken = data.access;
            refreshToken = data.refresh;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
            window.location.href = '/index.html';
        } else {
            alert('Login failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login.');
    }
}

// API call helper with token refresh
async function apiCall(url, options = {}) {
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    };
    try {
        let response = await fetch(url, options);
        if (!response.ok && response.status === 401) {
            const refreshed = await refreshAccessToken();
            if (!refreshed) {
                logout();
                throw new Error('Token refresh failed');
            }
            options.headers['Authorization'] = `Bearer ${accessToken}`;
            response = await fetch(url, options);
            if (!response.ok) {
                logout();
                throw new Error('Request failed after token refresh');
            }
        }
        return response;
    } catch (error) {
        console.error('API call error:', error);
        logout();
        throw error;
    }
}

// Check for unfinished quiz
async function checkUnfinishedQuiz() {
    const response = await apiCall(`${API_BASE_URL}/main/have_already_generated_quiz/`, { method: 'GET' });
    const data = await response.json();
    if (data.has_unfinished_quiz) {
        document.getElementById('popup').style.display = 'block';
    }
}

// Load popular topics
async function loadPopularTopics() {
    const response = await fetch(`${API_BASE_URL}/main/popular_topics/`, { method: 'GET' });
    const topics = await response.json();
    const list = document.getElementById('popularTopicsList');
    list.innerHTML = '';
    topics.forEach(topic => {
        const li = document.createElement('li');
        li.textContent = topic.name;
        list.appendChild(li);
    });
}

// Generate a new quiz
async function generateQuiz() {
    const prompt = document.getElementById('quizPrompt').value;
    const response = await apiCall(`${API_BASE_URL}/main/generate_quiz/`, {
        method: 'POST',
        body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    if (data.message) {
        alert(data.message);
    } else {
        firstQuestionId = data.question_id;
        document.getElementById('startQuizBtn').style.display = 'block';
    }
}

// Continue an unfinished quiz
async function continueQuiz() {
    const response = await apiCall(`${API_BASE_URL}/main/get_question_id/`, { method: 'GET' });
    const data = await response.json();
    firstQuestionId = data.question_id;
    document.getElementById('popup').style.display = 'none';
    startQuiz();
}

// Delete old quiz and start new
async function deleteAndNewQuiz() {
    await apiCall(`${API_BASE_URL}/main/delete_user_quiz/`, { method: 'POST' });
    document.getElementById('popup').style.display = 'none';
    document.getElementById('quizPrompt').value = '';
}

// Start the quiz
function startQuiz() {
    localStorage.setItem('currentQuestionId', firstQuestionId);
    window.location.href = '/quiz.html';
}

// Load current question
async function loadQuestion() {
    try {
        const response = await apiCall(`${API_BASE_URL}/main/questions/${currentQuestionId}/`, { method: 'GET' });
        const data = await response.json();

        // Check if quiz has ended
        if (data.message === "End of Quiz") {
            await computeQuizResult();
            return;
        }


        const questionText = data.question || data.name || Object.keys(data)[0]; // Fallback to first key if needed
        document.getElementById('questionText').textContent = questionText;

        const answersDiv = document.getElementById('answers');
        answersDiv.innerHTML = '';

        if (data.possible_answers.length !== 0) {
            const answers = data.possible_answers || data[Object.keys(data)[0]];
            answers.forEach((answer) => {
                const btn = document.createElement('button');
                btn.textContent = answer;
                btn.classList.add('answer-btn'); // Add class for styling
                btn.onclick = () => selectAnswer(btn, answer);
                answersDiv.appendChild(btn);
            });
        } else {
            const input = document.createElement('input');
            input.type = 'text';
            input.id = 'userAnswer';
            answersDiv.appendChild(input);
        }
    } catch (error) {
        console.error('Error loading question:', error);
        alert('Failed to load the question.');
    }
}

let selectedAnswer = null;
function selectAnswer(button, answer) {
    selectedAnswer = answer;
    const buttons = document.querySelectorAll('.answer-btn');
    buttons.forEach(btn => btn.classList.remove('selected'));
    // Add 'selected' class to the clicked button
    button.classList.add('selected');
}

// Submit answer and move to next question
async function submitAnswer() {
    const answer = selectedAnswer || document.getElementById('userAnswer')?.value;
    if (!answer) {
        alert('Please select or enter an answer.');
        return;
    }
    await apiCall(`${API_BASE_URL}/main/save_answer/`, {
        method: 'POST',
        body: JSON.stringify({ question: currentQuestionId, user_answer: answer})
    });
    currentQuestionId += 1;
    localStorage.setItem('currentQuestionId', currentQuestionId);
    await loadQuestion();
}

// Compute quiz result
async function computeQuizResult() {
    const response = await apiCall(`${API_BASE_URL}/main/compute_quiz/`, { method: 'POST' });
    const result = await response.json();
    alert(`Quiz completed! Your score: ${result.result}`);
    localStorage.removeItem('currentQuestionId');
    window.location.href = '/index.html';
}