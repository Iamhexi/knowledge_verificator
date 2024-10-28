<script>
    import { onMount } from "svelte";
    import { API_URL } from "../lib/config.js";
    import { goto } from '$app/navigation';

    let formData = { context: '', userAnswer: '', correctAnswer: '', question: '' };
    const minimumAnswerLength = 5;

    const handleSubmit = () => {
        const answerInput = document.querySelector('.answer-input');
        const answer = String(answerInput.value);
        if (answer.length < minimumAnswerLength) {
            alert(`Answer is too short. Minimum length: ${minimumAnswerLength}.`)
            return;
        }

        if (typeof window !== 'undefined') {
            sessionStorage.setItem('formData', JSON.stringify(formData));
            goto('/evaluate');
        }
  };

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

    /**
     * Make Ctrl + Enter send a form.
	 * @param {{ key: any; }} event
	 */
    function handleKeyDown(event) {
        // @ts-ignore
        if (event.ctrlKey && event.key === 'Enter') {
            handleSubmit();
        }
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
<form on:submit|preventDefault={handleSubmit}>
    <p>
        <b>Question:</b>
        <br>
        {question}
    </p>
    <input type="text" bind:value={formData.question} hidden readonly/>
    <input type="text" bind:value={formData.context} hidden readonly/>
    <input type="text" bind:value={formData.correctAnswer} hidden readonly/>
    <label>
        <p><b>Your answer:</b></p>
        <textarea
            class="answer-input"
            bind:value={formData.userAnswer}
            on:keydown={handleKeyDown}
            required
            autofocus
        ></textarea>
    </label>
    <button type="submit">&rarr;</button>
    </form>
{/if}


<style>
    label > p {
        /* padding: 10px; */
        display: block;
    }

    label {
        height: 10vh;
    }

    .answer-input {
        width: 80%;
        height: 10rem;
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

</style>
