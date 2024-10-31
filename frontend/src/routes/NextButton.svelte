<script>
	import { createEventDispatcher } from 'svelte';
	import Tooltip from './Tooltip.svelte';
	const dispatch = createEventDispatcher();

	export let content = '→';
	export let toolipText = 'Go to the next step.';
</script>

<Tooltip title={toolipText}>
	<button
		class="next-button"
		type="submit"
		on:click={() => {
			dispatch('click');
		}}
	>
		{content}
	</button>
</Tooltip>

<style>
	.next-button {
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: gray;
		color: white;
		border: none;
		line-height: 4rem;
		height: 4rem;
		width: 20%;
		min-width: 4rem;
		border-radius: 5px;
		font-size: 2rem;
	}

	.next-button:hover {
		cursor: pointer;
	}
</style>
