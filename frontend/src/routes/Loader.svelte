<script>
    import { writable } from 'svelte/store';
    import { Stretch } from 'svelte-loading-spinners';
	import { showErrorMessage } from '$lib/utils';
	import NextButton from './NextButton.svelte';

    // Async callback to be called by a click.
    export let callback = async () => {return new Promise(resolve => setTimeout(resolve, 1000)); };
    export let content = "";
    export let toolipText = "";
    export let parameters = [];

    const loading = writable(false);

    /**
	 * Wrap an async callback with a spinner whilst it loads.
	 */
    async function provideLoader() {
        loading.set(true);
        let data = null;
        try {
            data = await callback(...parameters);
        } catch (error) {
            showErrorMessage(`Error executing ${callback} with parameters: ${parameters}.`);
        } finally {
            loading.set(false);
        }
    }
</script>

{#if $loading}
    <div class="loading-overlay">
        <Stretch size="60" color="black" unit="px" duration="1s" />
    </div>
{/if}

<NextButton toolipText={toolipText} on:click={provideLoader} content={content}/>

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
</style>
