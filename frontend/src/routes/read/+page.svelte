<script>
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import NextButton from "../NextButton.svelte";
	import { loadFormData } from "$lib/utils";

    let formData = [];
    onMount(() => {
        formData = loadFormData();
    });

</script>
<h1>Read a paragraph</h1>
<p>{formData.context}</p>
<NextButton on:click={() => goto('/answer')}></NextButton>
