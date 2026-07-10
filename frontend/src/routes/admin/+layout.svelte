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

    /* =========================================
       LIGHT THEME OVERRIDES FOR ADMIN PANEL
    ========================================= */
    :global(html.theme-light) {
        background-color: #faf8f5 !important;
        color: #2c2420 !important;
    }

    :global(html.theme-light .bg-luxury-black) {
        background-color: #faf8f5 !important;
        color: #2c2420 !important;
    }

    :global(html.theme-light .bg-luxury-dark\/40),
    :global(html.theme-light .bg-luxury-dark\/60) {
        background-color: #f4ede1 !important;
    }

    :global(html.theme-light .bg-luxury-card),
    :global(html.theme-light .bg-luxury-card\/30),
    :global(html.theme-light .bg-luxury-card\/60),
    :global(html.theme-light .bg-luxury-card\/25),
    :global(html.theme-light .bg-luxury-card\/5) {
        background-color: #ffffff !important;
        color: #2c2420 !important;
    }

    :global(html.theme-light .bg-luxury-gold\/5) {
        background-color: #fbf8f2 !important;
    }

    :global(html.theme-light .bg-luxury-black\/40) {
        background-color: #f7f5f0 !important;
    }

    :global(html.theme-light .border-luxury-border),
    :global(html.theme-light .border-luxury-border\/80),
    :global(html.theme-light .border-luxury-border\/60),
    :global(html.theme-light .border-luxury-border\/50),
    :global(html.theme-light .border-luxury-border\/40),
    :global(html.theme-light .border-luxury-border\/30),
    :global(html.theme-light .border-luxury-border\/20) {
        border-color: #ddd5c8 !important;
    }

    :global(html.theme-light .border-l),
    :global(html.theme-light .border-r),
    :global(html.theme-light .border-b),
    :global(html.theme-light .border-t) {
        border-color: #e5dfd5 !important;
    }

    :global(html.theme-light .text-white) {
        color: #2c2420 !important;
    }

    :global(html.theme-light .text-gray-400),
    :global(html.theme-light .text-gray-500) {
        color: #6b5446 !important;
    }

    :global(html.theme-light .text-luxury-accent) {
        color: #483d39 !important;
    }

    :global(html.theme-light .text-luxury-gold) {
        color: #9e8877 !important;
    }

    :global(html.theme-light input),
    :global(html.theme-light select) {
        background-color: #ffffff !important;
        color: #2c2420 !important;
        border-color: #ddd5c8 !important;
    }

    :global(html.theme-light input::placeholder) {
        color: #a39287 !important;
    }

    :global(html.theme-light .bg-luxury-gold) {
        background-color: #9e8877 !important;
        color: #ffffff !important;
    }

    :global(html.theme-light .text-luxury-black) {
        color: #2c2420 !important;
    }
</style>
