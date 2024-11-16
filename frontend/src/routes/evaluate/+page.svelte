<script>
	import { onMount } from 'svelte';
	import { API_URL } from '../../lib/config.js';
	import { loadFormData, showErrorMessage, saveFormData, generateQuestion } from '../../lib/utils.js';
	import NextButton from '../NextButton.svelte';
	import { goto } from '$app/navigation';
	import Loader from '../Loader.svelte';
	import { Stretch } from 'svelte-loading-spinners';
	import { navigating } from '$app/stores'

	let formData = [];
	let evaluation = null;

	/**
	 * Fetch an evaluation of a user's answer from the API.
	 * @param {string} context
	 * @param {string} userAnswer
	 */
	async function evaluateAnswer(context, userAnswer) {
		const body = {
			context: context,
			user_answer: userAnswer
		};

		const options = {
			method: 'POST',
			body: JSON.stringify(body),
			headers: {
				'Content-Type': 'application/json' // Make sure to set the content type
			}
		};

		const endpoint = `${API_URL}/evaluate_answer`;
		const response = await fetch(endpoint, options);
		const result = await response.json();

		if (!result.data) {
			showErrorMessage(result.message);
			return;
		}
		return result.data.evaluation;
	}

	let isLoading = false;
	onMount(async () => {
		isLoading = true;
		formData = loadFormData();
		evaluation = await evaluateAnswer(formData.context, formData.userAnswer);
		isLoading = false;
	});

	/**
	 * Generate a feedback header based on the evaluation.
	 * @param {string} evaluation
	 * @returns {string|null}
	 */
	function getHeader(evaluation) {
		if (evaluation === 'entailment') {
			return 'Correct answer';
		} else if (evaluation === 'neutral') {
			return 'Unassociated answer';
		} else if (evaluation === 'contradiction') {
			return 'Wrong answer';
		}
		return null;
	}

	/**
	 * Generate a feedback paragraph based on the evaluation.
	 * @param {string} evaluation
	 * @returns {string}
	 */
	function getParagraph(evaluation) {
		const feedbackMessages = {
			entailment: 'Your answer is correct. Well done!',
			neutral:
				'Your answer does not seems to tackle the question. It is not necessarily wrong. Try to rephrase your answer.',
			contradiction: 'Your answer is wrong. Revise the learning material and try again.'
		};

		return (
			feedbackMessages[evaluation] ||
			'No evaluation provided. Please ensure that the evaluation is valid.'
		);
	}
</script>

{#if isLoading}
    <div class="loading-overlay">
        <Stretch size="60" color="black" unit="px" duration="1s" />
    </div>
{/if}

{#if evaluation}
	<main class="feedback-wrapper">
		<header><h1>Feedback</h1></header>
		<p class="feedback-evaluation {evaluation}">
			<b>{getHeader(evaluation)}</b>
			<br />
			{getParagraph(evaluation)}
		</p>
		<p><b>Question:</b> {formData.question}</p>
		<p><b>Your answer:</b> {formData.userAnswer}</p>
		<p><b>The suggested answer:</b> {formData.correctAnswer}</p>
		<p><b>The context:</b> {formData.context}</p>
	</main>

	<div class="button-organiser">
		<Loader
			callback={async () => {
				formData.answer = '';
				formData.question = '';
				saveFormData(formData);

				await generateQuestion(formData.context);
						goto('/read');
			}}
			content="↻"
			toolipText="Another question from the same learning material."
		/>
		<NextButton
			on:click={() => {
				goto('/');
			}}
			content="➔"
			toolipText="Switch to a different learning material."
		></NextButton>
	</div>
{/if}

<style>
    .loading-overlay {
        top: 0;
        left: 0;
        z-index: 999;
        width: 100vw;
        height: 100vh;
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }

	.feedback-wrapper {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		justify-content: space-between;
	}

	.feedback-wrapper p {
		padding: 1rem;
		border: 1px solid black;
	}

	.feedback-evaluation {
		border-radius: 5px;
		text-align: center;
		line-height: 2rem;
		border-width: 1px;
		border-style: solid;
	}

	.feedback-evaluation.entailment {
		background-color: #d4edda;
		color: #155724;
		border: 1px solid #c3e6cb;
	}

	.feedback-evaluation.contradiction {
		background-color: #f8d7da;
		color: #721c24;
		border: 1px solid #f5c6cb;
	}

	.feedback-evaluation.neutral {
		background-color: #fff3cd;
		color: #856404;
		border: 1px solid #ffeeba;
	}

	.button-organiser {
		margin: 2rem;
		display: flex;
		justify-content: space-around;
	}
</style>
