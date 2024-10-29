<script>
    import { onMount } from "svelte";
    import { API_URL } from "../lib/config.js";
	import LearningMaterial from "./LearningMaterial.svelte";
	import { loadFormData, saveFormData } from "$lib/utils.js";
	import { goto } from "$app/navigation";

    let formData = [];
    let learningMaterials = [];
    onMount(async function () {
        formData = loadFormData();
        const endpoint = `${API_URL}/materials`;
        const response = await fetch(endpoint);
        const result = await response.json();
        learningMaterials = result.data;
    });

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

        saveFormData(formData);
    }

</script>

<h1>Database of learning materials</h1>
{#each learningMaterials as material}
    <div class="learning-materials">
        {#each material.paragraphs as paragraph}
            <LearningMaterial
                title={material.title}
                bind:content={paragraph}
                onButtonClick={
                    async () => {
                        await generateQuestion(paragraph);
                        goto('/read');
                    }
                }
            >
            </LearningMaterial>
        {/each}
    </div>
{/each}

<style>
    .learning-materials {
        margin: 50px 0;
        display: flex;
        align-items: center;
        flex-direction: column;
        width: 100%;
    }

</style>
