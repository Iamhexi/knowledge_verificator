<script>
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

    const minimumAnswerLength = 5;

    let formData = { context: '', userAnswer: '', correctAnswer: '', question: '' };
    /**
         * @type {string|null}
         */
    let evaluation = null;

    function receiveFormData() {
        if (typeof window !== 'undefined' && sessionStorage.getItem('formData')) {
        // @ts-ignore
        formData = JSON.parse(sessionStorage.getItem('formData'));
        }
    }

    onMount(async () => {
        await receiveFormData();
        formData.userAnswer = '';
    });

    const handleSubmit = () => {
        const answerInput = document.querySelector('.answer-input');
        const answer = String(answerInput.value);
        if (answer.length < minimumAnswerLength) {
            alert(`Answer is too short. Minimum length: ${minimumAnswerLength}.`)
            return;
        }

        if (typeof window !== 'undefined') {
            sessionStorage.setItem('formData', JSON.stringify(formData));
            goto('/evaluate');
        }
  };

    /**
     * Make Ctrl + Enter send a form.
	 * @param {{ key: any; }} event
	 */
     function handleKeyDown(event) {
        // @ts-ignore
        if (event.ctrlKey && event.key === 'Enter') {
            handleSubmit();
        }
    }
</script>

<form on:submit|preventDefault={handleSubmit}>
    <p>
        <b>Question:</b>
        <br>
        {formData.question}
    </p>
    <input type="text" bind:value={formData.question} hidden readonly/>
    <input type="text" bind:value={formData.context} hidden readonly/>
    <input type="text" bind:value={formData.correctAnswer} hidden readonly/>
    <label>
        <p><b>Your answer:</b></p>
        <textarea
            class="answer-input"
            bind:value={formData.userAnswer}
            on:keydown={handleKeyDown}
            required
            autofocus
        ></textarea>
    </label>
    <button type="submit">&rarr;</button>
</form>
