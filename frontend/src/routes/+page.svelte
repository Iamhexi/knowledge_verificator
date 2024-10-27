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
	 * @param {string} context
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
                    {#if question}
                        <p>Question: {question}</p>
                    {/if}
                </div>
            {/each}
            <!-- <p><b>Tags</b>: {material.tags.join(', ')}</p> -->
        </div>
    {/each}
{:else}
    <p>Question: {question}</p>
    <form method="post" action="/evaluate">
        <label>
            <p>Your answer: </p>
            <textarea class="answer-input" autofocus></textarea>
        </label>
        <input value="Check the answer" type="submit">
    </form>
{/if}
<!-- <pre>{JSON.stringify(learningMaterials, null, 2)}</pre> -->


<style>
    label > p {
        /* padding: 10px; */
        display: block;
    }

    input[type="submit"] {
        display: block;
    }

    label {
        height: 10vh;
    }

    .answer-input {
        width: 80%;
        height: 10rem;
    }

    h1 {
        text-transform: uppercase;
    }

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

    button {
        /* height: 3.5rem; */
        /* line-height: 3.5rem; */
        text-align: center;
        text-decoration: none;
        border: 1px solid gray;
        border-radius: 5px;
        padding: 0.5rem;
        background-color: darkgray;
        width: 20%;
        font-size: 2rem;
    }

    button:hover {
        cursor: pointer;
    }
</style>
