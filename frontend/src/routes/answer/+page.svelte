<script>
	import { onMount } from "svelte";
	import NextButton from "../NextButton.svelte";
	import { loadFormData, saveFormData } from "$lib/utils";
	import { goto } from "$app/navigation";

    const minimumAnswerLength = 5;

    let formData = [];
    onMount(() => {
        formData = loadFormData();
        formData.userAnswer = '';
    });

    const handleSubmit = () => {
        const answerInput = document.querySelector('.answer-input');
        const answer = String(answerInput.value);
        if (answer.length < minimumAnswerLength) {
            alert(`Answer is too short. Minimum length: ${minimumAnswerLength}.`)
            return;
        }

        saveFormData(formData);
        goto('/evaluate');
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
    <NextButton></NextButton>
</form>
