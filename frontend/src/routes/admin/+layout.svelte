<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let loading = true;
    let authenticated = false;

    $: isLoginPage = $page.url.pathname === '/admin/login';

    function checkAuth() {
        if (typeof window !== 'undefined') {
            const token = localStorage.getItem('unic_admin_token');
            if (token) {
                authenticated = true;
            } else {
                authenticated = false;
            }
            
            loading = false;

            // Apply routing redirects
            if (!authenticated && !isLoginPage) {
                goto('/admin/login');
            } else if (authenticated && isLoginPage) {
                goto('/admin/crm');
            }
        }
    }

    onMount(() => {
        checkAuth();
    });

    // Reactively watch url pathname changes
    $: if (typeof window !== 'undefined' && $page.url.pathname) {
        checkAuth();
    }
</script>

{#if loading}
    <div class="loading-wrap">
        <div class="spinner"></div>
    </div>
{:else}
    <slot />
{/if}

<style>
    .loading-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: #faf8f5;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 2px solid #ddd5c8;
        border-top-color: #9e8877;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
