<script>
  import { onMount } from "svelte";
  import { API_URL } from "../../lib/config.js";
  import { showErrorMessage, disableLoader, enableLoader } from "../../lib/utils.js"
	import { goto } from "$app/navigation";

  let formData = { context: '', userAnswer: '', correctAnswer: '', question: '' };
  /**
	 * @type {string|null}
	 */
  let evaluation = null;

  function receiveFormData() {
    if (typeof window !== 'undefined' && sessionStorage.getItem('formData')) {
      // @ts-ignore
      formData = JSON.parse(sessionStorage.getItem('formData'));
    }
  }

  /**
   * Fetch an evaluation of a user's answer from the API.
   * @param {string} context
   * @param {string} userAnswer
   */
  async function evaluateAnswer(context, userAnswer) {
    const body = {
      context: context,
      user_answer: userAnswer,
    };

    const options = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
          'Content-Type': 'application/json' // Make sure to set the content type
      }
    };

    const endpoint = `${API_URL}/evaluate_answer`;
    const response = await fetch(endpoint, options);
    const result = await response.json();

    if (!result.data){
      showErrorMessage(result.message);
      return;
    }
    return result.data.evaluation;
}

onMount(async () => {
  enableLoader();
  receiveFormData();
  evaluation = await evaluateAnswer(formData.context, formData.userAnswer);
  disableLoader();
});
</script>

{#if formData.context && formData.userAnswer && formData.correctAnswer }
  <p>The context: {formData.context}</p>
  <p>Your answer: {formData.userAnswer}</p>
  <p>The correct answer: {formData.correctAnswer}</p>
  <p>Question: {formData.question}</p>
  <p>Evaluation: {evaluation}</p>

  <a href="/">Change a paragraph</a>
{/if}
