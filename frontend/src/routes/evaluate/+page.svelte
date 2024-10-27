<!-- src/routes/pageB.svelte -->
<script>
    let formData = { context: '', answer: '' };

    if (typeof window !== 'undefined' && sessionStorage.getItem('formData')) {
      formData = JSON.parse(sessionStorage.getItem('formData'));
    }
</script>

{#if formData.context && formData.answer }
    <p>Context: {formData.context}</p>
    <p>Answer: {formData.answer}</p>
{/if}
