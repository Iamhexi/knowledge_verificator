
/**
 * Show an error message.
 * @param {string} message
 */
export function showErrorMessage(message) {
    alert(`Error: ${message}.`);
}

export function enableLoader() {
    // TODO: Implement loader.
}

export function disableLoader() {
    // TODO: Implement disabling loader.
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
