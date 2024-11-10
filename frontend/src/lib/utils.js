import { API_URL } from "./config";

/**
 * Show an error message.
 * @param {string} message
 */
export function showErrorMessage(message) {
    alert(`Error: ${message}.`);
}

export function loadFormData() {
    if (typeof window !== 'undefined' && sessionStorage.getItem('formData')) {
        return JSON.parse(sessionStorage.getItem('formData'));
    }
    return { context: '', userAnswer: '', correctAnswer: '', question: '' };
}

/**
 * @param {any} formData
    // export let formData = { context: '', userAnswer: '', correctAnswer: '', question: '' };
 */
export function saveFormData(formData) {
    if (typeof window !== 'undefined') {
        sessionStorage.setItem('formData', JSON.stringify(formData));
    }
}

 /**
    * Fetch an API endpoint to generate a question based on the provided context.
    * @param {string} context Full paragraph of text used as the context.
    */
export async function generateQuestion(context) {
    let formData = loadFormData();

    const body = {
        context: context,
    };
    const options = {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json' // Make sure to set the content type
        }
    };
    const endpoint = `${API_URL}/generate_question`
    const response = await fetch(endpoint, options);
    const result = await response.json();

    formData.context = context;
    formData.correctAnswer = result.data.answer;
    formData.question = result.data.question;

    saveFormData(formData);
}
