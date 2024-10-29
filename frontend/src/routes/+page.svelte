<script>
    import { onMount } from "svelte";
    import { API_URL } from "../lib/config.js";
    import { goto } from '$app/navigation';

    let formData = { context: '', userAnswer: '', correctAnswer: '', question: '' };

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

    /**
     * @param {string} text
     * @param {number} maxLength
     */
    function truncate(text, maxLength = 20) {
        const appendix = maxLength < text.length ? '...' : '';
        return `${text.slice(0, maxLength - 1)}${appendix}`;
    }

    /**
	 * @type {null}
	 */
    let question = null;

    /**
     * Fetch an API endpoint to generate a question based on the provided context.
	 * @param {string} context Full paragraph of text used as the context.
	 */
    async function generateQuestion(context) {
        const body = {
            context: context,
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json' // Make sure to set the content type
            }
        };
        const endpoint = `${API_URL}/generate_question`
        const response = await fetch(endpoint, options);
        const result = await response.json();

        formData.context = context;
        formData.correctAnswer = result.data.answer;
        formData.question = result.data.question;

        question = result.data.question;
    }



</script>

<h1>Database of learning materials</h1>
{#if !question}
    {#each learningMaterials as material}
        <div class="learning-material">
            {#each material.paragraphs as paragraph}
                <div class="paragraph-to-learn">
                    <p>The paragraph from <i>{material.title}</i>: {truncate(paragraph, 200)}</p>
                    <button on:click={() => generateQuestion(paragraph)}>&rarr;</button>
                </div>
            {/each}
        </div>
    {/each}
{:else}
    <p>Read a paragraph</p>
    <p>{formData.context}</p>
    <button on:click={() => goto('/answer')}>&rarr;</button>
{/if}


<style>
    .learning-material {
        margin: 50px 0;
        display: flex;
        align-items: center;
        flex-direction: column;
        width: 100%;
    }

    .paragraph-to-learn {
        border: 1px dashed black;
        margin: 1rem auto;
        padding: 1rem;
        width: 80%;
        max-height: 5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .paragraph-to-learn p {
        text-align: justify;
        margin-right: 1rem;
    }

</style>
