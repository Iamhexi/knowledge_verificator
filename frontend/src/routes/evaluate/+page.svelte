<script>
  import { onMount } from "svelte";
  import { API_URL } from "../../lib/config.js";
  import { showErrorMessage, disableLoader, enableLoader } from "../../lib/utils.js"

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


	/**
   * Generate a feedback header based on the evaluation.
	 * @param {string} evaluation
   * @returns {string|null}
	 */
function getHeader(evaluation) {
  if (evaluation === 'entailment') {
    return 'Correct answer';
  } else if (evaluation === 'neutral') {
    return 'Unassociated answer';
  } else if (evaluation === 'contradiction') {
    return 'Wrong answer';
  }
  return null;
}

/**
 * Generate a feedback paragraph based on the evaluation.
 * @param {string} evaluation
 * @returns {string}
 */
 function getParagraph(evaluation) {
  const feedbackMessages = {
    entailment: 'Your answer is correct. Well done!',
    neutral: 'Your answer does not seems to tackle the question. It is not necessarily wrong. Try to rephrase your answer.',
    contradiction: 'Your answer is wrong. Revise the learning material and try again.'
  };

  return feedbackMessages[evaluation] || 'No evaluation provided. Please ensure that the evaluation is valid.';
}

</script>

{#if evaluation }
  <main class="feedback-wrapper">
    <header><h1>Feedback</h1></header>
    <p class="feedback-evaluation {evaluation}">
      <b>{getHeader(evaluation)}</b>
      <br>
      {getParagraph(evaluation)}
    </p>
    <p><b>Question:</b> {formData.question}</p>
    <p><b>Your answer:</b> {formData.userAnswer}</p>
    <p><b>The correct answer:</b> {formData.correctAnswer}</p>
    <p><b>The context:</b> {formData.context}</p>
  </main>

  <a href="/">Change a paragraph</a>
{/if}

<style>
  .feedback-wrapper {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: space-between;
  }

  .feedback-wrapper p {
    padding: 1rem;
    border: 1px solid black;
  }

  .feedback-evaluation {
    border-radius: 5px;
    text-align: center;
    line-height: 2rem;
    border-width: 1px;
    border-style: solid;
  }

  .feedback-evaluation.entailment {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .feedback-evaluation.contradiction {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .feedback-evaluation.neutral {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
  }

</style>
