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
            console.log(`Parameters: ${parameters}`);
            data = await callback(...parameters);
        } catch (error) {
            showErrorMessage(`Error executing ${callback} with parameters: ${parameters}.`);
        } finally {
            loading.set(false);
            // return data;
        }
    }
</script>

{#if $loading}
    <Stretch size="60" color="#FF3E00" unit="px" duration="1s" />
{/if}

<NextButton toolipText={toolipText} on:click={provideLoader} content={content}/>
