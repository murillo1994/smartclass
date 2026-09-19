<script>
    import { api } from '../../services/api';
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';
    let error = '';
    let loading = false;

    async function handleLogin() {
        if (!username || !password) {
            error = 'Preencha todos os campos';
            return;
        }
        
        loading = true;
        error = '';

        try {
            const res = await api.login(username, password);
            if (res.user && res.user.role === 'superadmin') {
                goto('/admin/superadmin');
            } else {
                goto('/admin/inbox');
            }
        } catch (err) {
            error = err.message || 'Erro ao efetuar login';
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>Evolution CRM SaaS — Acesso ao Painel</title>
</svelte:head>

<div class="login-page">
    <div class="login-card">
        <div class="brand">
            <h1 style="font-size: 1.6rem; font-weight: 800; color: #483d39; letter-spacing: -0.02em; margin: 0;">EVOLUTION CRM</h1>
            <span class="subtitle">Multi-Tenant WhatsApp SaaS</span>
        </div>

        <form on:submit|preventDefault={handleLogin} class="login-form">
            {#if error}
                <div class="error-box">
                    <span>{error}</span>
                </div>
            {/if}

            <div class="input-group">
                <label for="username">E-mail ou Usuário</label>
                <input 
                    type="text" 
                    id="username" 
                    bind:value={username} 
                    placeholder="ex: admin@empresa.com ou super@crm.com"
                    required
                    disabled={loading}
                />
            </div>

            <div class="input-group">
                <label for="password">Senha</label>
                <input 
                    type="password" 
                    id="password" 
                    bind:value={password} 
                    placeholder="Digite sua senha"
                    required
                    disabled={loading}
                />
            </div>

            <button type="submit" class="btn-submit" disabled={loading}>
                {#if loading}
                    Conectando...
                {:else}
                    Acessar Painel
                {/if}
            </button>
        </form>
    </div>
</div>

<style>
    .login-page {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: radial-gradient(circle at center, #faf8f5 0%, #ede6dd 100%);
        padding: 1.5rem;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(158, 136, 119, 0.25);
        padding: 3.5rem 2.5rem;
        border-radius: 12px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 10px 30px rgba(44, 36, 32, 0.08);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
    }

    .brand {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        width: 100%;
    }

    .logo {
        width: 170px;
        height: auto;
        object-fit: contain;
    }

    .subtitle {
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #9e8877;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    .login-form {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        width: 100%;
    }

    .error-box {
        background: #fdf2f2;
        border: 1px solid #f8b4b4;
        color: #9b1c1c;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        text-align: center;
        animation: shake 0.3s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-4px); }
        75% { transform: translateX(4px); }
    }

    .input-group {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        width: 100%;
    }

    .input-group label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6b5446;
        font-weight: 600;
    }

    .input-group input {
        width: 100%;
        padding: 0.85rem 1rem;
        border: 1px solid #ddd5c8;
        background: #ffffff;
        color: #2c2420;
        border-radius: 6px;
        font-size: 0.9rem;
        outline: none;
        box-sizing: border-box;
        transition: border-color 0.25s, box-shadow 0.25s;
    }

    .input-group input:focus {
        border-color: #9e8877;
        box-shadow: 0 0 0 3px rgba(158, 136, 119, 0.15);
    }

    .btn-submit {
        width: 100%;
        background: #483d39;
        color: #faf8f5;
        border: 1px solid #483d39;
        padding: 0.95rem;
        border-radius: 6px;
        font-size: 0.8rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.12em;
        cursor: pointer;
        transition: background-color 0.2s, border-color 0.2s, opacity 0.2s;
        margin-top: 0.5rem;
    }

    .btn-submit:hover:not(:disabled) {
        background: #2c2420;
        border-color: #2c2420;
    }

    .btn-submit:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .btn-back {
        font-size: 0.72rem;
        color: #9e8877;
        text-decoration: none;
        transition: color 0.2s;
        letter-spacing: 0.05em;
    }

    .btn-back:hover {
        color: #483d39;
    }
</style>
