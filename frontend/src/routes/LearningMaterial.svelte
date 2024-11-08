<script>
	import Loader from './Loader.svelte';
	export let title = 'Default title';
	export let content = 'Default content';
	export let maxLength = 200;
	export let onButtonClick;

	/**
	 * Truncate a text to a desired length.
	 * @param {string} text
	 * @param {number} maxLength
	 */
	function truncate(text, maxLength = 20) {
		const appendix = maxLength < text.length ? '...' : '';
		return `${text.slice(0, maxLength - 1)}${appendix}`;
	}
</script>

<div class="learning-material">
	<p>The paragraph from <i>{title}</i>: {truncate(content, maxLength)}</p>
	<Loader callback={onButtonClick} />
</div>

<style>
	.learning-material {
		border: 1px dashed black;
		margin: 1rem auto;
		padding: 1rem;
		width: 80%;
		max-height: 5rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.learning-material p {
		text-align: justify;
		margin-right: 1rem;
	}
</style>
