<script>
	import { onMount } from 'svelte';
	import NextButton from '../NextButton.svelte';
	import { loadFormData, saveFormData } from '$lib/utils';
	import { goto } from '$app/navigation';

	const minimumAnswerLength = 5;

	let formData = [];
	onMount(() => {
		formData = loadFormData();
		formData.userAnswer = '';
	});

	const handleSubmit = () => {
		const answerInput = document.querySelector('.long-text-input');
		const answer = answerInput ? String(answerInput.value) : '';
		if (answer.length < minimumAnswerLength) {
			alert(`Answer is too short. Minimum length: ${minimumAnswerLength}.`);
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

<main>
    <h1>Answer the question</h1>
	<form on:submit|preventDefault={handleSubmit}>
		<p>
			<b>Question:</b>
			<br/>
			{formData.question}
			<br/>
			<br/>
		</p>
		<input type="text" bind:value={formData.question} hidden readonly />
		<input type="text" bind:value={formData.context} hidden readonly />
		<input type="text" bind:value={formData.correctAnswer} hidden readonly />
		<label>
			<p><b>Your answer:</b></p>
			<textarea
				class="long-text-input"
				bind:value={formData.userAnswer}
				on:keydown={handleKeyDown}
                placeholder="Your answer goes here..."
				required
				autofocus
			></textarea>
		</label>
		<NextButton></NextButton>
	</form>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        width: 100vw;
		padding: 2rem;
    }

    p {
        margin-bottom: .5rem;
    }
</style>
