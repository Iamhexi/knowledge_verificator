<script>
	import { onMount } from 'svelte';
	import { API_URL } from '../lib/config.js';
	import LearningMaterial from './LearningMaterial.svelte';
	import { generateQuestion } from '$lib/utils.js';
	import { goto } from '$app/navigation';
	import NextButton from './NextButton.svelte';
	import Loader from './Loader.svelte';

	let text = '';
	let learningMaterials = [];
	onMount(async function () {
		const endpoint = `${API_URL}/materials`;
		const response = await fetch(endpoint);
		const result = await response.json();
		learningMaterials = result.data;
	});
</script>

<div class="learning-materials">
	<h1>Database of learning materials</h1>
	{#each learningMaterials as material}
		{#each material.paragraphs as paragraph}
			<LearningMaterial
				title={material.title}
				bind:content={paragraph}
				onButtonClick={async () => {
					await generateQuestion(paragraph);
					goto('/read');
				}}
			></LearningMaterial>
		{/each}
	{/each}
</div>
<Loader/>
<div class="text-insertion-wrapper">
	<h1>My learning material</h1>
	<p>Insert a paragraph you want to learn:</p>
	<label>
		<textarea
			class="long-text-input"
			bind:value={text}
			placeholder="Your learning material goes here..."
		></textarea>
	</label>
	<NextButton
		on:click={async () => {
			const minimumInputLength = 15;
			if (text.length < minimumInputLength) {
				alert(`Cannot use a learning material of length shorter than ${minimumInputLength} characters.`)
				return;
			}
			await generateQuestion(text);
			goto('/read');
		}}
	></NextButton>
</div>

<style>
	.learning-materials h1 {
		padding-bottom: 1rem;
	}

	.text-insertion-wrapper,
	.learning-materials {
		display: flex;
		flex-direction: column;
		padding: 2rem;
		width: 100vw;
	}

	p {
		margin-top: 0.5rem;
	}
</style>
