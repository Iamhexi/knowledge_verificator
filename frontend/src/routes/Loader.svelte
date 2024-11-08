<script>
    import { writable } from 'svelte/store';
    import { Stretch } from 'svelte-loading-spinners';
	import { API_URL } from '$lib/config';
	import { showErrorMessage } from '$lib/utils';

    // Async callback to be
    let callback = async () => {return new Promise(resolve => setTimeout(resolve, 1000)); };
    let parameters = [];
    const loading = writable(false);

    /**
     * Wrap an async callback with a spinner whilst it loads.
     * @param {function} callback Function to be called in callback.
     */
    async function provideLoader() {
        loading.set(true);
        let data = null;
        try {
            data = await callback(...parameters);
            // data = await response.json();
        } catch (error) {
            // showErrorMessage(`Error while retrieving data from ${endpoint}: ${error}`);
        } finally {
            loading.set(false);
            // return data;
        }
    }
</script>

{#if $loading}
    <Stretch size="60" color="#FF3E00" unit="px" duration="1s" />
{/if}

<button on:click={provideLoader}>Fetch Data</button>
