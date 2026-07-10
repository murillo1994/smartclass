<script>
    import Header from '../components/Header.svelte';

    // Premium procedures with images
    const treatments = [
        {
            name: "Terapia Capilar",
            desc: "Tratamento especializado para queda de cabelo e saúde do couro cabeludo.",
            img: "/images/queda-de-cabelo.jpg"
        },
        {
            name: "Toxina Botulínica",
            desc: "Suavização precisa de linhas de expressão e rugas dinâmicas.",
            img: "/images/botox-unic.jpg"
        },
        {
            name: "Estímulo de Colágeno",
            desc: "Aplicações avançadas para sustentação, firmeza e elasticidade da pele.",
            img: "/images/colágeno-1.jpg"
        },
        {
            name: "Rejuvenescimento Facial",
            desc: "Tratamentos integrados para a restauração e vitalidade da pele madura.",
            img: "/images/PELE MADURA.jpg"
        },
        {
            name: "Flacidez de Pálpebras",
            desc: "Procedimentos direcionados para sustentação da região dos olhos.",
            img: "/images/pálpebras-flácidas.jpg"
        },
        {
            name: "Remoção de Tatuagem",
            desc: "Tecnologia a laser segura e eficiente para despigmentação.",
            img: "/images/remoção-de-tatuagem.jpg"
        }
    ];

    const whatsappNumber = "5511999999999";
    const whatsappMessage = "Olá! Gostaria de agendar uma consulta de avaliação na Unic Clinic.";
    const whatsappUrl = `https://api.whatsapp.com/send?phone=${whatsappNumber}&text=${encodeURIComponent(whatsappMessage)}`;
</script>

<div class="min-h-screen bg-luxury-black text-white flex flex-col font-sans selection:bg-luxury-gold selection:text-luxury-black">
    <!-- Header with custom Unic Clinic Logo -->
    <Header logo="/logos/unic_clinic_logo_1_claro.png" />

    <!-- Hero Section (Descubra a leveza de se cuidar) -->
    <section class="relative min-h-[90vh] flex items-center justify-center overflow-hidden px-6 py-24">
        <!-- Background Image overlay -->
        <div class="absolute inset-0 z-0">
            <img 
                src="/images/d30d12f522074d70f09e3697bbda97f8.jpg" 
                alt="Unic Clinic Estética" 
                class="w-full h-full object-cover opacity-25 filter brightness-[0.4]"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-luxury-black via-luxury-black/70 to-transparent"></div>
        </div>

        <div class="max-w-4xl text-center z-10 space-y-8">
            <span class="text-[10px] tracking-[0.4em] uppercase text-luxury-gold font-semibold bg-luxury-gold/10 px-4 py-2 rounded-full border border-luxury-gold/20">
                Unic Clinic • Estética Médica de Alto Padrão
            </span>
            
            <h1 class="text-4xl sm:text-7xl font-serif tracking-wide text-white leading-tight">
                Descubra a leveza <br />
                <span class="italic text-luxury-gold">de se cuidar</span>
            </h1>
            
            <p class="text-xs sm:text-sm text-gray-400 max-w-xl mx-auto leading-relaxed font-light">
                Abordagem integral, segura e personalizada para realçar sua essência e promover saúde e vitalidade.
            </p>

            <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
                <a 
                    href={whatsappUrl} 
                    target="_blank"
                    rel="noopener noreferrer"
                    class="w-full sm:w-auto bg-luxury-gold text-luxury-black hover:bg-luxury-gold/90 font-bold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase shadow-lg shadow-luxury-gold/10 hover:scale-[1.02]"
                >
                    Agende uma Consulta
                </a>
                <a 
                    href="#tratamentos" 
                    class="w-full sm:w-auto border border-luxury-border hover:border-luxury-gold text-white font-semibold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase bg-luxury-card/25 hover:bg-luxury-card/50"
                >
                    Conhecer os Tratamentos
                </a>
            </div>
        </div>
        
        <!-- Bottom scroll indicator line -->
        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center space-y-2 opacity-50">
            <span class="text-[9px] tracking-widest uppercase">Descubra</span>
            <div class="w-px h-12 bg-gradient-to-b from-luxury-gold to-transparent animate-pulse"></div>
        </div>
    </section>

    <!-- Treatments section (Jet Listing Grid style) -->
    <section id="tratamentos" class="py-24 px-6 bg-luxury-dark/45 border-y border-luxury-border/30 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center space-y-3">
                <span class="text-[10px] tracking-widest uppercase text-luxury-gold font-semibold">Portfólio de Cuidados</span>
                <h2 class="text-3xl sm:text-4xl font-serif tracking-wide text-luxury-accent">Procedimentos & Tratamentos</h2>
                <div class="w-12 h-0.5 bg-luxury-gold mx-auto mt-4"></div>
            </div>

            <!-- Jet-Listing Grid emulation -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {#each treatments as treat}
                    <div class="bg-luxury-card border border-luxury-border/60 rounded-2xl overflow-hidden flex flex-col hover:border-luxury-gold transition duration-300 group">
                        <!-- Image Container with zoom hover -->
                        <div class="relative h-56 overflow-hidden">
                            <img 
                                src={treat.img} 
                                alt={treat.name} 
                                class="w-full h-full object-cover group-hover:scale-105 transition duration-500"
                            />
                            <div class="absolute inset-0 bg-gradient-to-t from-luxury-card/90 via-transparent to-transparent"></div>
                        </div>

                        <!-- Card Body -->
                        <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                            <div class="space-y-2">
                                <h3 class="font-serif text-lg text-white group-hover:text-luxury-gold transition duration-200">{treat.name}</h3>
                                <p class="text-xs text-gray-400 leading-relaxed font-light">{treat.desc}</p>
                            </div>
                            <div class="pt-4 border-t border-luxury-border/20 flex items-center justify-between text-[11px] text-gray-500 font-mono">
                                <span>Consulta Exclusiva</span>
                                <a 
                                    href={whatsappUrl} 
                                    target="_blank" 
                                    class="text-luxury-gold font-sans uppercase tracking-wider font-semibold hover:underline"
                                >
                                    Saber Mais →
                                </a>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </section>

    <!-- Propósito Section -->
    <section class="py-24 px-6 bg-luxury-black relative flex items-center justify-center text-center">
        <div class="max-w-3xl mx-auto space-y-8">
            <div class="flex justify-center">
                <img 
                    src="/logos/unic_clinic_icone_claro.png" 
                    alt="Unic Clinic Ícone" 
                    class="h-16 w-16 object-contain opacity-80"
                />
            </div>
            <p class="font-serif text-xl sm:text-2xl tracking-wide text-luxury-accent leading-relaxed">
                "Um propósito simples e admirável: aprimorar a qualidade de vida, a saúde da pele e restaurar a autoconfiança de nossos pacientes com naturalidade e sofisticação."
            </p>
            <div class="w-px h-16 bg-gradient-to-b from-luxury-gold to-transparent mx-auto"></div>
        </div>
    </section>

    <!-- Espaço Projetado Section -->
    <section class="py-24 px-6 bg-luxury-dark/30 border-t border-luxury-border/30 relative">
        <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-12 items-center">
            <div class="md:col-span-6 space-y-6">
                <h2 class="text-3xl sm:text-4xl font-serif tracking-wide text-luxury-accent">Um espaço projetado para o seu bem-estar</h2>
                <p class="text-xs sm:text-sm text-gray-400 font-light leading-relaxed">
                    Com um time de profissionais altamente experientes, nossa clínica oferece uma abordagem integrada para promover sua saúde, beleza e vitalidade. Da harmonização facial refinada aos mais modernos tratamentos capilares e tecnologias regenerativas, cada detalhe de nossa estrutura foi pensado para oferecer uma experiência única, acolhedora e personalizada.
                </p>
                <div class="pt-4">
                    <a 
                        href={whatsappUrl} 
                        target="_blank"
                        rel="noopener noreferrer"
                        class="inline-flex items-center space-x-3 bg-luxury-gold text-luxury-black hover:bg-luxury-gold/90 font-bold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase"
                    >
                        <span>Conheça a clínica</span>
                        <span>→</span>
                    </a>
                </div>
            </div>
            <div class="md:col-span-6">
                <div class="border border-luxury-border p-2 rounded-2xl bg-luxury-card/30">
                    <img 
                        src="/images/64140b8b2d4a42ed834c0d94f6cfa4f1.jpg" 
                        alt="Estrutura Unic Clinic" 
                        class="rounded-xl w-full h-[400px] object-cover"
                    />
                </div>
            </div>
        </div>
    </section>

    <!-- Olhar Atencioso (Renata Moedim / Romana Style) -->
    <section class="py-24 px-6 bg-luxury-black relative">
        <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-12 items-center">
            <div class="md:col-span-6 order-last md:order-first">
                <div class="border border-luxury-border p-2 rounded-2xl bg-luxury-card/30">
                    <img 
                        src="/images/3d1e607e20a69ba4fc7d9f5fc109dc6e.jpg" 
                        alt="Corpo Clínico Unic Clinic" 
                        class="rounded-xl w-full h-[400px] object-cover"
                    />
                </div>
            </div>
            <div class="md:col-span-6 space-y-6">
                <h2 class="text-3xl sm:text-4xl font-serif tracking-wide text-luxury-accent">Olhar atencioso e individualizado</h2>
                <p class="text-xs sm:text-sm text-gray-400 font-light leading-relaxed">
                    Nossa equipe clínica acredita que a verdadeira beleza reside na harmonia e na naturalidade. Cada consulta de avaliação é um diagnóstico detalhado que estuda as proporções e necessidades de cada paciente. Sob responsabilidade técnica qualificada, buscamos entregar tratamentos precisos que trazem rejuvenescimento sem descaracterizar a sua expressão.
                </p>
                <div class="pt-4">
                    <a 
                        href={whatsappUrl} 
                        target="_blank"
                        rel="noopener noreferrer"
                        class="inline-flex items-center space-x-3 bg-transparent border border-luxury-gold text-luxury-gold hover:bg-luxury-gold hover:text-luxury-black font-bold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase"
                    >
                        <span>Falar com Especialista</span>
                        <span>→</span>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-16 px-6 border-t border-luxury-border/30 bg-luxury-dark/80 relative">
        <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 items-start text-xs text-gray-400">
            <!-- Left col: Logo and description -->
            <div class="space-y-4">
                <img 
                    src="/logos/unic_clinic_logo_1_claro.png" 
                    alt="Unic Clinic Logo" 
                    class="h-10 object-contain"
                />
                <p class="leading-relaxed font-light">
                    Responsável Técnico Médico:<br />
                    Dra. Renata Moedim<br />
                    CRM-SP: 101.553 | RQE: 113772<br />
                    CREMESP 101.553
                </p>
            </div>

            <!-- Middle col: Address -->
            <div class="space-y-3">
                <h4 class="font-serif text-sm text-white tracking-wider">Endereço</h4>
                <p class="leading-relaxed font-light font-mono">
                    Rua Canadá, 215, Jd. América<br />
                    São Paulo - SP | CEP 01436-000
                </p>
            </div>

            <!-- Right col: Contact / WhatsApp -->
            <div class="space-y-3">
                <h4 class="font-serif text-sm text-white tracking-wider">Contato & Redes</h4>
                <p class="leading-relaxed font-light">
                    Telefone: (11) 3303-0022<br />
                    WhatsApp: (11) 99999-9999
                </p>
                <div class="pt-2 flex items-center space-x-4">
                    <a 
                        href="https://www.instagram.com/clinica.romana" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="text-gray-500 hover:text-luxury-gold transition duration-200"
                    >
                        Instagram
                    </a>
                    <span class="text-luxury-border/30">•</span>
                    <a 
                        href={whatsappUrl} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="text-gray-500 hover:text-luxury-gold transition duration-200"
                    >
                        WhatsApp
                    </a>
                </div>
            </div>
        </div>

        <div class="max-w-6xl mx-auto mt-12 pt-8 border-t border-luxury-border/10 text-center text-[10px] text-gray-600">
            <p>&copy; 2026 Unic Clinic. Todos os direitos reservados. Desenvolvido com sofisticação.</p>
        </div>
    </footer>
</div>
