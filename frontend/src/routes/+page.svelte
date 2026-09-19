<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    onMount(() => {
        goto('/admin/login');
    });
</script>

<div class="redirect-wrap">
    <div class="spinner"></div>
    <p>Redirecionando para o login...</p>
</div>

<style>
    .redirect-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: #faf8f5;
        gap: 1rem;
        color: #6b5446;
        font-family: system-ui, -apple-system, sans-serif;
    }

    .spinner {
        width: 36px;
        height: 36px;
        border: 2px solid #ddd5c8;
        border-top-color: #9e8877;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
