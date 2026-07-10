<script>
    import Header from '../components/Header.svelte';

    const whatsappNumber = "5511999999999";
    const whatsappMessage = "Olá! Vim do site da Unic Clinic e gostaria de agendar uma consulta de avaliação.";
    const whatsappUrl = `https://api.whatsapp.com/send?phone=${whatsappNumber}&text=${encodeURIComponent(whatsappMessage)}`;

    const treatments = [
        { name: "Terapia Capilar", img: "/images/queda-de-cabelo.jpg" },
        { name: "Toxina Botulínica", img: "/images/botox-unic.jpg" },
        { name: "Estímulo de Colágeno", img: "/images/colágeno-1.jpg" },
        { name: "Rejuvenescimento Facial", img: "/images/PELE MADURA.jpg" },
        { name: "Flacidez de Pálpebras", img: "/images/pálpebras-flácidas.jpg" },
        { name: "Remoção de Tatuagem", img: "/images/remoção-de-tatuagem.jpg" },
    ];
    import { onMount } from 'svelte';

    let purposeVisible = false;
    let purposeEl;

    onMount(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    purposeVisible = true;
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        if (purposeEl) {
            observer.observe(purposeEl);
        }

        return () => observer.disconnect();
    });
</script>

<svelte:head>
    <title>Unic Clinic — Descubra a leveza de se cuidar</title>
</svelte:head>

<div class="page-wrap">
    <Header logo="/logos/unic_clinic_logo_marrom_hd.png" />

    <!-- ===== HERO ===== -->
    <section class="hero">
        <div class="hero-bg">
            <img src="/images/d30d12f522074d70f09e3697bbda97f8.jpg" alt="Unic Clinic Estética Médica" />
            <div class="hero-overlay"></div>
        </div>
        <div class="hero-content">
            <p class="hero-label">Unic Clinic • Estética Médica de Alto Padrão</p>
            <h1 class="hero-title">
                Descubra a leveza<br/>
                <em>de se cuidar</em>
            </h1>
            <p class="hero-subtitle">
                Abordagem integral, segura e personalizada para realçar<br class="hide-mobile"/> 
                sua essência e promover saúde e vitalidade.
            </p>
            <div class="hero-actions">
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-primary">
                    Agende uma consulta
                </a>
                <a href="#tratamentos" class="btn-ghost">
                    Conhecer os tratamentos →
                </a>
            </div>
        </div>
        <div class="hero-scroll">
            <span>Descubra</span>
            <div class="scroll-line"></div>
        </div>
    </section>

    <!-- ===== TREATMENTS GRID ===== -->
    <section id="tratamentos" class="section section-cream-dark">
        <div class="container">
            <div class="section-header">
                <p class="section-label">Portfólio de Cuidados</p>
                <h2 class="section-title">Procedimentos &amp; Tratamentos</h2>
                <p class="section-desc">
                    Com um time de profissionais qualificados, nossa clínica oferece<br class="hide-mobile"/>
                    uma abordagem integral para promover sua saúde e vitalidade.
                </p>
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="section-cta">
                    Conhecer os tratamentos →
                </a>
            </div>

            <div class="treatments-grid">
                {#each treatments as treat}
                    <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="treatment-card">
                        <div class="treatment-img-wrap">
                            <img src={treat.img} alt={treat.name} class="treatment-img" />
                        </div>
                        <div class="treatment-body">
                            <h3 class="treatment-name">{treat.name}</h3>
                            <span class="treatment-arrow">→</span>
                        </div>
                    </a>
                {/each}
            </div>
        </div>
    </section>

    <!-- ===== PURPOSE ===== -->
    <section bind:this={purposeEl} class="section section-white text-center purpose-section">
        <div class="purpose-wrap">
            <img src="/logos/unic_clinic_icone_cinza.png" alt="Unic Clinic" class="purpose-icon" class:animate={purposeVisible} />
            <p class="purpose-text">
                "Um propósito simples e admirável: aprimorar a qualidade de vida,<br class="hide-mobile"/>
                a saúde da pele e restaurar a autoconfiança de nossos pacientes<br class="hide-mobile"/>
                com naturalidade e sofisticação."
            </p>
            <div class="purpose-line"></div>
        </div>
    </section>

    <!-- ===== SPACE ===== -->
    <section id="sobre" class="section section-cream-dark split-section">
        <div class="container split-container">
            <div class="split-image">
                <img src="/images/64140b8b2d4a42ed834c0d94f6cfa4f1.jpg" alt="Estrutura Unic Clinic" />
            </div>
            <div class="split-content">
                <p class="section-label">Nosso Espaço</p>
                <h2 class="section-title">Um espaço projetado<br/>para o seu bem-estar</h2>
                <p class="split-desc">
                    Com um time de profissionais altamente experientes, nossa clínica oferece uma abordagem integrada para promover sua saúde, beleza e vitalidade. Da harmonização facial refinada aos mais modernos tratamentos capilares e tecnologias regenerativas, cada detalhe foi pensado para oferecer uma experiência única, acolhedora e personalizada.
                </p>
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-primary">
                    Conheça a clínica →
                </a>
            </div>
        </div>
    </section>

    <!-- ===== DOCTOR ===== -->
    <section class="section section-white split-section">
        <div class="container split-container reverse">
            <div class="split-content">
                <p class="section-label">Nossa Equipe</p>
                <h2 class="section-title">Olhar atencioso<br/>e individualizado</h2>
                <p class="split-desc">
                    Nossa equipe clínica acredita que a verdadeira beleza reside na harmonia e na naturalidade. Cada consulta de avaliação é um diagnóstico detalhado que estuda as proporções e necessidades de cada paciente. Sob responsabilidade técnica qualificada, buscamos tratamentos precisos que trazem rejuvenescimento sem descaracterizar sua expressão.
                </p>
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-outline">
                    Falar com especialista →
                </a>
            </div>
            <div class="split-image">
                <img src="/images/3d1e607e20a69ba4fc7d9f5fc109dc6e.jpg" alt="Corpo Clínico Unic Clinic" />
            </div>
        </div>
    </section>

    <!-- ===== CTA BANNER ===== -->
    <section id="contato" class="section cta-banner">
        <div class="cta-content">
            <p class="section-label" style="color: #c4b9ad;">Agende agora</p>
            <h2 style="font-size: clamp(1.8rem, 4vw, 3rem); color: #faf8f5; font-weight: 300; letter-spacing: -0.01em; margin: 0.75rem 0 2rem;">
                Pronto para se cuidar com <em style="font-style: italic; font-weight: 400;">sofisticação</em>?
            </h2>
            <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-light">
                Agendar consulta de avaliação →
            </a>
        </div>
    </section>

    <!-- ===== FOOTER ===== -->
    <footer class="footer">
        <div class="container footer-grid">
            <div class="footer-col">
                <img src="/logos/unic_clinic_logo_claro_hd.png" alt="Unic Clinic Logo" class="footer-logo" />
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Endereço</h4>
                <p class="footer-text">
                    R. Euclides Miragaia, 145, Sl 415<br/>
                    Centro, São José dos Campos - SP<br/>
                    CEP 12245-820
                </p>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Contato &amp; Redes</h4>
                <p class="footer-text">
                    Telefone: (11) 3303-0022<br/>
                    WhatsApp: (11) 99999-9999
                </p>
                <div class="footer-links">
                    <a href="https://www.instagram.com/unic_clinic" target="_blank" rel="noopener noreferrer" class="footer-link">@unic_clinic</a>
                    <span style="color: #ddd5c8;">•</span>
                    <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="footer-link">WhatsApp</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 Unic Clinic. Todos os direitos reservados.</p>
        </div>
    </footer>
</div>

<style>
    /* =========================================
       PAGE WRAPPER
    ========================================= */
    .page-wrap {
        background: #faf8f5;
        color: #2c2420;
        font-family: 'Poppins', sans-serif;
        min-height: 100vh;
    }

    /* =========================================
       HERO
    ========================================= */
    .hero {
        position: relative;
        min-height: 92vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .hero-bg {
        position: absolute;
        inset: 0;
        z-index: 0;
    }

    .hero-bg img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.55) saturate(0.8);
    }

    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(44, 36, 32, 0.75) 0%, rgba(44, 36, 32, 0.25) 60%, transparent 100%);
    }

    .hero-content {
        position: relative;
        z-index: 1;
        text-align: center;
        max-width: 720px;
        padding: 2rem;
        animation: fadeInUp 0.8s ease forwards;
    }

    .hero-label {
        font-size: 0.68rem;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        color: #e8e0d5;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(2.8rem, 7vw, 5.5rem);
        font-weight: 300;
        color: #faf8f5;
        line-height: 1.1;
        letter-spacing: -0.01em;
        margin: 0 0 1.5rem;
    }

    .hero-title em {
        font-style: italic;
        font-weight: 400;
        color: #e8d5c0;
    }

    .hero-subtitle {
        font-size: 0.9rem;
        color: #c4b9ad;
        line-height: 1.7;
        font-weight: 300;
        margin-bottom: 2.5rem;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
    }

    .hero-scroll {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        opacity: 0.5;
    }

    .hero-scroll span {
        font-size: 0.6rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: #faf8f5;
    }

    .scroll-line {
        width: 1px;
        height: 48px;
        background: linear-gradient(to bottom, #faf8f5, transparent);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    /* =========================================
       BUTTONS
    ========================================= */
    .btn-primary {
        display: inline-block;
        background: #483d39;
        color: #faf8f5;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 600;
        padding: 0.9rem 2rem;
        text-decoration: none;
        border: 1.5px solid #483d39;
        border-radius: 2px;
        transition: all 0.25s;
    }

    .btn-primary:hover {
        background: #2c2420;
        border-color: #2c2420;
    }

    .btn-ghost {
        display: inline-block;
        background: transparent;
        color: #faf8f5;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 500;
        padding: 0.9rem 2rem;
        text-decoration: none;
        border: 1.5px solid rgba(250, 248, 245, 0.4);
        border-radius: 2px;
        transition: all 0.25s;
    }

    .btn-ghost:hover {
        border-color: #faf8f5;
        background: rgba(250, 248, 245, 0.1);
    }

    .btn-outline {
        display: inline-block;
        background: transparent;
        color: #483d39;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 600;
        padding: 0.85rem 1.8rem;
        text-decoration: none;
        border: 1.5px solid #483d39;
        border-radius: 2px;
        transition: all 0.25s;
    }

    .btn-outline:hover {
        background: #483d39;
        color: #faf8f5;
    }

    .btn-light {
        display: inline-block;
        background: #faf8f5;
        color: #483d39;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 700;
        padding: 1rem 2.5rem;
        text-decoration: none;
        border: 1.5px solid #faf8f5;
        border-radius: 2px;
        transition: all 0.25s;
    }

    .btn-light:hover {
        background: transparent;
        color: #faf8f5;
    }

    /* =========================================
       SECTIONS
    ========================================= */
    .section {
        padding: 6rem 1.5rem;
    }

    .section-white { background: #ffffff; }
    .section-cream-dark { background: #f2ede6; }

    .container {
        max-width: 1100px;
        margin: 0 auto;
    }

    .section-header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 4rem;
    }

    .section-label {
        font-size: 0.65rem;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        color: #9e8877;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(1.8rem, 3.5vw, 2.8rem);
        font-weight: 300;
        color: #2c2420;
        line-height: 1.2;
        letter-spacing: -0.01em;
        margin: 0 0 1rem;
    }

    .section-desc {
        font-size: 0.88rem;
        color: #6b5446;
        line-height: 1.8;
        font-weight: 300;
        margin: 0 0 1.5rem;
    }

    .section-cta {
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #483d39;
        font-weight: 600;
        text-decoration: none;
        transition: opacity 0.2s;
    }

    .section-cta:hover { opacity: 0.7; }

    .text-center { text-align: center; }
    .text-center .section-header { align-items: center; }

    /* =========================================
       TREATMENTS GRID
    ========================================= */
    .treatments-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1px;
        background: #ddd5c8;
        border: 1px solid #ddd5c8;
    }

    @media (max-width: 640px) {
        .treatments-grid { grid-template-columns: 1fr; }
    }

    .treatment-card {
        background: #ffffff;
        text-decoration: none;
        display: block;
        overflow: hidden;
        transition: background 0.2s;
        position: relative;
    }

    .treatment-card:hover { background: #faf8f5; }

    .treatment-img-wrap {
        height: 260px;
        overflow: hidden;
    }

    .treatment-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
        display: block;
    }

    .treatment-card:hover .treatment-img { transform: scale(1.04); }

    .treatment-body {
        padding: 1.5rem 1.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #f2ede6;
    }

    .treatment-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        color: #2c2420;
        margin: 0;
        letter-spacing: 0.02em;
    }

    .treatment-arrow {
        font-size: 1rem;
        color: #9e8877;
        transition: transform 0.2s, color 0.2s;
    }

    .treatment-card:hover .treatment-arrow {
        transform: translateX(4px);
        color: #483d39;
    }

    /* =========================================
       PURPOSE
    ========================================= */
    .purpose-section {
        overflow: hidden;
    }

    .purpose-wrap {
        max-width: 680px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }

    .purpose-icon {
        width: 110px;
        height: 110px;
        object-fit: contain;
        opacity: 0;
        transform: translateX(180px);
        transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 1.2s ease-out;
        will-change: transform, opacity;
    }

    .purpose-icon.animate {
        opacity: 0.8;
        transform: translateX(0);
    }

    .purpose-text {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(1rem, 2.2vw, 1.25rem);
        font-weight: 300;
        color: #483d39;
        line-height: 1.8;
        letter-spacing: 0.01em;
        margin: 0;
    }

    .purpose-line {
        width: 1px;
        height: 64px;
        background: linear-gradient(to bottom, #c4b9ad, transparent);
        margin-top: 0.5rem;
    }

    /* =========================================
       SPLIT SECTIONS
    ========================================= */
    .split-section {}

    .split-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5rem;
        align-items: center;
    }

    .split-container.reverse { direction: rtl; }
    .split-container.reverse > * { direction: ltr; }

    @media (max-width: 768px) {
        .split-container { grid-template-columns: 1fr; gap: 2.5rem; }
        .split-container.reverse { direction: ltr; }
    }

    .split-image {
        overflow: hidden;
        border-radius: 2px;
    }

    .split-image img {
        width: 100%;
        height: 480px;
        object-fit: cover;
        display: block;
        transition: transform 0.6s ease;
    }

    .split-image:hover img { transform: scale(1.02); }

    .split-content {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .split-desc {
        font-size: 0.88rem;
        color: #6b5446;
        line-height: 1.9;
        font-weight: 300;
    }

    /* =========================================
       CTA BANNER
    ========================================= */
    .cta-banner {
        background: #483d39;
        text-align: center;
        padding: 7rem 1.5rem;
    }

    .cta-content {
        max-width: 600px;
        margin: 0 auto;
    }

    /* =========================================
       FOOTER
    ========================================= */
    .footer {
        background: #2c2420;
        padding: 5rem 1.5rem 2rem;
    }

    .footer-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 3rem;
        margin-bottom: 3rem;
    }

    @media (max-width: 768px) {
        .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
    }

    .footer-col {}

    .footer-logo {
        width: 180px;
        height: auto;
        object-fit: contain;
        margin-bottom: 1.25rem;
        display: block;
    }

    .footer-heading {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #c4b9ad;
        font-weight: 600;
        margin: 0 0 1rem;
    }

    .footer-text {
        font-size: 0.8rem;
        color: #9e8877;
        line-height: 1.8;
        font-weight: 300;
        margin: 0;
    }

    .footer-links {
        margin-top: 1rem;
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    .footer-link {
        font-size: 0.75rem;
        color: #9e8877;
        text-decoration: none;
        transition: color 0.2s;
    }

    .footer-link:hover { color: #e8e0d5; }

    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.07);
        padding-top: 1.5rem;
        text-align: center;
    }

    .footer-bottom p {
        font-size: 0.72rem;
        color: #6b5446;
        margin: 0;
    }

    /* =========================================
       RESPONSIVE
    ========================================= */
    @media (max-width: 640px) {
        .hide-mobile { display: none; }
        .section { padding: 4rem 1.25rem; }
        .split-image img { height: 280px; }
    }

    /* =========================================
       ANIMATIONS
    ========================================= */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
