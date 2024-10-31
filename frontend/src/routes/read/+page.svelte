<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import NextButton from '../NextButton.svelte';
	import { generateQuestion, loadFormData } from '$lib/utils';

	let formData = [];
	onMount(() => {
		formData = loadFormData();
	});
</script>

<main>
	<h1>Read a paragraph</h1>
	<p>{formData.context}</p>
	<NextButton on:click={() => goto('/answer')}></NextButton>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		padding: 2rem;
	}

	main p {
		margin: 1rem 0rem;
		padding: 1rem 1rem;
		text-align: justify;
		background-color: rgb(206, 197, 197);
		line-height: 2;
		font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
		font-size: 1.2rem;
	}
</style>
