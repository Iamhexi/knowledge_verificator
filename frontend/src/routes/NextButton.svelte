<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    export let content = '→';


</script>

<button class="next-button" type="submit" on:click={() => {dispatch('click')}}>
    {content}
</button>

<style>
    .next-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: gray;
        color: white;
        border: none;
        line-height: 4rem;
        height: 4rem;
        width: 20%;
        border-radius: 5px;
        font-size: 2rem;
        padding-bottom: 1rem; /* Centering an arrow with padding. */
    }

    .next-button:hover {
        cursor: pointer;
    }
</style>
