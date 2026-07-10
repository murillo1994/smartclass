<script>
    import Header from '../components/Header.svelte';
    import { onMount } from 'svelte';

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

    // Parallax on hero image
    let heroImg;
    let scrollY = 0;

    // Intersection Observer for scroll animations
    onMount(() => {
        // Parallax
        const onScroll = () => {
            scrollY = window.scrollY;
            if (heroImg) {
                heroImg.style.transform = `translateY(${scrollY * 0.3}px)`;
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });

        // Fade in on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    observer.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });

        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

        return () => {
            window.removeEventListener('scroll', onScroll);
            observer.disconnect();
        };
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
            <img bind:this={heroImg} src="/images/d30d12f522074d70f09e3697bbda97f8.jpg" alt="Unic Clinic Estética Médica" />
            <div class="hero-overlay"></div>
        </div>
        <div class="hero-content">
            <p class="hero-label reveal">Unic Clinic • Estética Médica de Alto Padrão</p>
            <h1 class="hero-title reveal" style="transition-delay: 0.15s;">
                Descubra a leveza<br/>
                <em>de se cuidar</em>
            </h1>
            <p class="hero-subtitle reveal" style="transition-delay: 0.3s;">
                Abordagem integral, segura e personalizada para realçar<br class="hide-mobile"/>
                sua essência e promover saúde e vitalidade.
            </p>
            <div class="hero-actions reveal" style="transition-delay: 0.45s;">
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

    <!-- ===== STATS BAR ===== -->
    <div class="stats-bar">
        <div class="stat reveal">
            <span class="stat-num">+5.000</span>
            <span class="stat-label">Pacientes Atendidos</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat reveal" style="transition-delay:0.1s;">
            <span class="stat-num">10+</span>
            <span class="stat-label">Anos de Experiência</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat reveal" style="transition-delay:0.2s;">
            <span class="stat-num">15+</span>
            <span class="stat-label">Procedimentos Especializados</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat reveal" style="transition-delay:0.3s;">
            <span class="stat-num">100%</span>
            <span class="stat-label">Responsabilidade Técnica Médica</span>
        </div>
    </div>

    <!-- ===== TREATMENTS GRID ===== -->
    <section id="tratamentos" class="section section-cream-dark">
        <div class="container">
            <div class="section-header reveal">
                <p class="section-label">Portfólio de Cuidados</p>
                <h2 class="section-title">Procedimentos &amp; Tratamentos</h2>
                <p class="section-desc">
                    Com um time de profissionais qualificados, nossa clínica oferece<br class="hide-mobile"/>
                    uma abordagem integral para promover sua saúde e vitalidade.
                </p>
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="section-cta">
                    Ver todos os tratamentos →
                </a>
            </div>

            <div class="treatments-grid">
                {#each treatments as treat, i}
                    <a href={whatsappUrl} target="_blank" rel="noopener noreferrer"
                       class="treatment-card reveal"
                       style="transition-delay: {i * 0.08}s;">
                        <div class="treatment-img-wrap">
                            <img src={treat.img} alt={treat.name} class="treatment-img" />
                            <div class="treatment-img-overlay"></div>
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
    <section class="section section-white text-center">
        <div class="purpose-wrap">
            <img src="/logos/unic_clinic_icone_cinza.png" alt="Unic Clinic" class="purpose-icon reveal" />
            <p class="purpose-text reveal" style="transition-delay:0.15s;">
                "Um propósito simples e admirável: aprimorar a qualidade de vida,<br class="hide-mobile"/>
                a saúde da pele e restaurar a autoconfiança de nossos pacientes<br class="hide-mobile"/>
                com naturalidade e sofisticação."
            </p>
            <div class="purpose-line reveal" style="transition-delay:0.3s;"></div>
        </div>
    </section>

    <!-- ===== SPACE (split) ===== -->
    <section id="sobre" class="section section-cream-dark split-section">
        <div class="container split-container">
            <div class="split-image reveal">
                <img src="/images/64140b8b2d4a42ed834c0d94f6cfa4f1.jpg" alt="Estrutura Unic Clinic" />
            </div>
            <div class="split-content reveal" style="transition-delay:0.2s;">
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

    <!-- ===== DOCTOR (split reversed) ===== -->
    <section class="section section-white split-section">
        <div class="container split-container reverse">
            <div class="split-content reveal">
                <p class="section-label">Nossa Equipe</p>
                <h2 class="section-title">Olhar atencioso<br/>e individualizado</h2>
                <p class="split-desc">
                    Nossa equipe clínica acredita que a verdadeira beleza reside na harmonia e na naturalidade. Cada consulta de avaliação é um diagnóstico detalhado que estuda as proporções e necessidades de cada paciente. Sob responsabilidade técnica qualificada, buscamos tratamentos precisos que trazem rejuvenescimento sem descaracterizar sua expressão.
                </p>
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-outline">
                    Falar com especialista →
                </a>
            </div>
            <div class="split-image reveal" style="transition-delay:0.2s;">
                <img src="/images/3d1e607e20a69ba4fc7d9f5fc109dc6e.jpg" alt="Corpo Clínico Unic Clinic" />
            </div>
        </div>
    </section>

    <!-- ===== FULL-BLEED IMAGE BANNER (Leger style) ===== -->
    <section class="full-banner">
        <div class="full-banner-bg">
            <img src="/images/7a2a9aa81952d6c4bf676d1ecf784d9d.jpg" alt="Unic Clinic ambiente" />
            <div class="full-banner-overlay"></div>
        </div>
        <div class="full-banner-content reveal">
            <p class="section-label" style="color:#c4b9ad;">Nossa Filosofia</p>
            <h2 style="font-family:'Montserrat',sans-serif; font-size:clamp(2rem,5vw,3.5rem); font-weight:300; color:#faf8f5; line-height:1.2; margin:1rem 0 2rem; letter-spacing:-0.01em;">
                Beleza que respeita<br/><em style="font-style:italic;font-weight:400;">quem você é</em>
            </h2>
            <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-light">
                Agende sua avaliação →
            </a>
        </div>
    </section>

    <!-- ===== CTA BANNER ===== -->
    <section id="contato" class="section cta-banner">
        <div class="cta-content">
            <p class="section-label reveal" style="color:#c4b9ad;">Agende agora</p>
            <h2 class="reveal" style="transition-delay:0.1s; font-family:'Montserrat',sans-serif; font-size:clamp(1.8rem,4vw,3rem); color:#faf8f5; font-weight:300; letter-spacing:-0.01em; margin:0.75rem 0 2rem;">
                Pronto para se cuidar com <em style="font-style:italic;font-weight:400;">sofisticação</em>?
            </h2>
            <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" class="btn-light reveal" style="transition-delay:0.2s;">
                Agendar consulta de avaliação →
            </a>
        </div>
    </section>

    <!-- ===== FOOTER ===== -->
    <footer class="footer">
        <div class="container footer-grid">
            <div class="footer-col">
                <img src="/logos/unic_clinic_logo_marrom_hd.png" alt="Unic Clinic Logo" class="footer-logo" />
                <p class="footer-text">
                    Responsável Técnico Médico:<br/>
                    Dra. Renata Moedim<br/>
                    CRM-SP: 101.553 | RQE: 113772<br/>
                    CREMESP 101.553
                </p>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Endereço</h4>
                <p class="footer-text">
                    Rua Canadá, 215, Jd. América<br/>
                    São Paulo - SP | CEP 01436-000
                </p>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Contato &amp; Redes</h4>
                <p class="footer-text">
                    Telefone: (11) 3303-0022<br/>
                    WhatsApp: (11) 99999-9999
                </p>
                <div class="footer-links">
                    <a href="https://www.instagram.com/unicclinic" target="_blank" rel="noopener noreferrer" class="footer-link">Instagram</a>
                    <span style="color:#3a2e2b;">•</span>
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
    /* ===== PAGE WRAPPER ===== */
    .page-wrap {
        background: #faf8f5;
        color: #2c2420;
        font-family: 'Poppins', sans-serif;
        min-height: 100vh;
    }

    /* ===== SCROLL REVEAL ===== */
    .reveal {
        opacity: 0;
        transform: translateY(28px);
        transition: opacity 0.75s ease, transform 0.75s ease;
    }
    .reveal.visible {
        opacity: 1;
        transform: translateY(0);
    }

    /* ===== HERO ===== */
    .hero {
        position: relative;
        min-height: 95vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .hero-bg {
        position: absolute;
        inset: 0;
        z-index: 0;
        overflow: hidden;
    }
    .hero-bg img {
        width: 100%;
        height: 120%;
        object-fit: cover;
        filter: brightness(0.52) saturate(0.75);
        will-change: transform;
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(44,36,32,0.8) 0%, rgba(44,36,32,0.2) 55%, transparent 100%);
    }
    .hero-content {
        position: relative;
        z-index: 1;
        text-align: center;
        max-width: 760px;
        padding: 2rem;
    }
    .hero-label {
        font-size: 0.65rem;
        letter-spacing: 0.38em;
        text-transform: uppercase;
        color: #e8e0d5;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(3rem, 8vw, 6rem);
        font-weight: 300;
        color: #faf8f5;
        line-height: 1.08;
        letter-spacing: -0.02em;
        margin: 0 0 1.5rem;
    }
    .hero-title em { font-style: italic; font-weight: 400; color: #e8d5c0; }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #c4b9ad;
        line-height: 1.75;
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
        opacity: 0.45;
    }
    .hero-scroll span {
        font-size: 0.58rem;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: #faf8f5;
    }
    .scroll-line {
        width: 1px;
        height: 48px;
        background: linear-gradient(to bottom, #faf8f5, transparent);
        animation: scrollPulse 2s ease-in-out infinite;
    }
    @keyframes scrollPulse {
        0%, 100% { opacity: 0.4; transform: scaleY(0.7); transform-origin: top; }
        50% { opacity: 1; transform: scaleY(1); }
    }

    /* ===== STATS BAR ===== */
    .stats-bar {
        background: #2c2420;
        padding: 2.5rem 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0;
    }
    .stat {
        text-align: center;
        padding: 0.5rem 3rem;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .stat-num {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.8rem;
        font-weight: 300;
        color: #e8d5c0;
        letter-spacing: -0.01em;
    }
    .stat-label {
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #9e8877;
        font-weight: 500;
    }
    .stat-divider {
        width: 1px;
        height: 40px;
        background: #3a2e2b;
    }
    @media (max-width: 640px) {
        .stat-divider { display: none; }
        .stat { padding: 0.75rem 1.5rem; }
        .stats-bar { gap: 0.5rem; }
    }

    /* ===== BUTTONS ===== */
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
    .btn-primary:hover { background: #2c2420; border-color: #2c2420; }

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
        border: 1.5px solid rgba(250,248,245,0.4);
        border-radius: 2px;
        transition: all 0.25s;
    }
    .btn-ghost:hover { border-color: #faf8f5; background: rgba(250,248,245,0.1); }

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
    .btn-outline:hover { background: #483d39; color: #faf8f5; }

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
    .btn-light:hover { background: transparent; color: #faf8f5; }

    /* ===== SECTIONS ===== */
    .section { padding: 6rem 1.5rem; }
    .section-white { background: #ffffff; }
    .section-cream-dark { background: #f2ede6; }

    .container { max-width: 1100px; margin: 0 auto; }

    .section-header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 4rem;
    }
    .section-label {
        font-size: 0.63rem;
        letter-spacing: 0.38em;
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
        line-height: 1.85;
        font-weight: 300;
        margin: 0 0 1.5rem;
    }
    .section-cta {
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #483d39;
        font-weight: 600;
        text-decoration: none;
        transition: opacity 0.2s;
        border-bottom: 1px solid currentColor;
        padding-bottom: 2px;
    }
    .section-cta:hover { opacity: 0.6; }
    .text-center { text-align: center; }
    .text-center .section-header { align-items: center; }

    /* ===== TREATMENTS GRID ===== */
    .treatments-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1px;
        background: #ddd5c8;
        border: 1px solid #ddd5c8;
    }
    @media (max-width: 768px) { .treatments-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 480px) { .treatments-grid { grid-template-columns: 1fr; } }

    .treatment-card {
        background: #ffffff;
        text-decoration: none;
        display: block;
        overflow: hidden;
        transition: background 0.25s;
        position: relative;
    }
    .treatment-card:hover { background: #faf8f5; }

    .treatment-img-wrap {
        height: 240px;
        overflow: hidden;
        position: relative;
    }
    .treatment-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        display: block;
    }
    .treatment-card:hover .treatment-img { transform: scale(1.06); }
    .treatment-img-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(44,36,32,0.3) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .treatment-card:hover .treatment-img-overlay { opacity: 1; }

    .treatment-body {
        padding: 1.25rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #f2ede6;
    }
    .treatment-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.88rem;
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
    .treatment-card:hover .treatment-arrow { transform: translateX(5px); color: #483d39; }

    /* ===== PURPOSE ===== */
    .purpose-wrap {
        max-width: 680px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }
    .purpose-icon { width: 56px; height: 56px; object-fit: contain; opacity: 0.55; }
    .purpose-text {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(1rem, 2.2vw, 1.2rem);
        font-weight: 300;
        color: #483d39;
        line-height: 1.85;
        letter-spacing: 0.01em;
        margin: 0;
    }
    .purpose-line {
        width: 1px;
        height: 60px;
        background: linear-gradient(to bottom, #c4b9ad, transparent);
    }

    /* ===== SPLIT SECTIONS ===== */
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
    .split-image { overflow: hidden; border-radius: 2px; }
    .split-image img {
        width: 100%;
        height: 480px;
        object-fit: cover;
        display: block;
        transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .split-image:hover img { transform: scale(1.03); }
    .split-content { display: flex; flex-direction: column; gap: 1.25rem; }
    .split-desc { font-size: 0.88rem; color: #6b5446; line-height: 1.9; font-weight: 300; }

    /* ===== FULL-BLEED BANNER (Leger style) ===== */
    .full-banner {
        position: relative;
        height: 65vh;
        min-height: 420px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .full-banner-bg {
        position: absolute;
        inset: 0;
    }
    .full-banner-bg img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.45) saturate(0.7);
    }
    .full-banner-overlay {
        position: absolute;
        inset: 0;
        background: rgba(44, 36, 32, 0.45);
    }
    .full-banner-content {
        position: relative;
        z-index: 1;
        text-align: center;
        max-width: 640px;
        padding: 2rem;
    }

    /* ===== CTA BANNER ===== */
    .cta-banner {
        background: #483d39;
        text-align: center;
        padding: 7rem 1.5rem;
    }
    .cta-content { max-width: 600px; margin: 0 auto; }

    /* ===== FOOTER ===== */
    .footer { background: #2c2420; padding: 5rem 1.5rem 2rem; }
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 3rem;
        margin-bottom: 3rem;
    }
    @media (max-width: 768px) { .footer-grid { grid-template-columns: 1fr; gap: 2rem; } }
    .footer-logo {
        height: 28px;
        object-fit: contain;
        margin-bottom: 1.25rem;
        filter: brightness(0.5) sepia(0.3);
        opacity: 0.7;
    }
    .footer-heading {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #c4b9ad;
        font-weight: 600;
        margin: 0 0 1rem;
    }
    .footer-text { font-size: 0.8rem; color: #9e8877; line-height: 1.8; font-weight: 300; margin: 0; }
    .footer-links { margin-top: 1rem; display: flex; gap: 0.75rem; align-items: center; }
    .footer-link { font-size: 0.75rem; color: #9e8877; text-decoration: none; transition: color 0.2s; }
    .footer-link:hover { color: #e8e0d5; }
    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.06);
        padding-top: 1.5rem;
        text-align: center;
    }
    .footer-bottom p { font-size: 0.7rem; color: #6b5446; margin: 0; }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 640px) {
        .hide-mobile { display: none; }
        .section { padding: 4rem 1.25rem; }
        .split-image img { height: 280px; }
        .full-banner { height: 55vh; }
    }
</style>
