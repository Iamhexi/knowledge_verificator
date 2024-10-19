<script>
    import { onMount } from "svelte";
    import { API_URL } from "../lib/config.js";

    /**
	 * @type {any[]}
	 */
    let learningMaterials = [];
    const endpoint = `${API_URL}/materials`;

    onMount(async function () {
        const response = await fetch(endpoint);
        const result = await response.json();
        learningMaterials = result.data;
    });
</script>

<h1>Database of learning materials</h1>
{#each learningMaterials as material}
    <div class="learning-material">
        {#each material.paragraphs as paragraph}
            <div class="paragraph-to-learn">
                <p>{material.title}: {paragraph}</p>
                <a href="">-></a>
            </div>
        {/each}
        <!-- <p><b>Tags</b>: {material.tags.join(', ')}</p> -->
    </div>
{/each}
<!-- <pre>{JSON.stringify(learningMaterials, null, 2)}</pre> -->


<style>
    h1 {
        text-transform: uppercase;
    }

    .learning-material {
        margin: 50px 10px;
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .paragraph-to-learn {
        border: 1px dashed black;
        margin: 1rem;
        padding: 1.2rem 2rem 2rem;
    }

    a {
        width: 100%;
        height: 3.5rem;
        line-height: 3.5rem;
        text-align: center;
        text-decoration: none;
        border: 1px solid gray;
        border-radius: 5px;
        padding: 0.5rem;
        background-color: darkgray;
        width: 100%;
        display: block;
    }

    a:visited {
        color: black;
    }

    a:hover {
        cursor: pointer;
    }
</style>
