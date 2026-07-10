<script>
    import Header from '../components/Header.svelte';

    // Premium Procedures list for display
    const procedures = [
        {
            name: "Toxina Botulínica (Botox)",
            desc: "Tratamento de precisão para suavização de rugas dinâmicas e linhas de expressão, mantendo a naturalidade da expressão facial.",
            duration: "30 min",
            price: "R$ 1.200"
        },
        {
            name: "Preenchimento Labial",
            desc: "Escultura e volumização labial com ácido hialurônico para restaurar o contorno, definição e simetria.",
            duration: "45 min",
            price: "R$ 1.500"
        },
        {
            name: "Harmonização Facial",
            desc: "Planejamento personalizado e integrado para realçar sua beleza natural e redefinir contornos de forma equilibrada.",
            duration: "60 min",
            price: "R$ 3.500"
        },
        {
            name: "Bioestimulador de Colágeno",
            desc: "Tratamento profundo contra a flacidez facial e corporal, estimulando a produção natural de sustentação da pele.",
            duration: "45 min",
            price: "R$ 2.200"
        }
    ];

    const whatsappNumber = "5511999999999";
    const whatsappMessage = "Olá! Gostaria de agendar uma consulta de avaliação na Unic Clinic.";
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;
</script>

<div class="min-h-screen bg-luxury-black text-white flex flex-col font-sans selection:bg-luxury-gold selection:text-luxury-black">
    <Header />

    <!-- Hero Section -->
    <section class="relative min-h-[85vh] flex items-center justify-center overflow-hidden py-24 px-6">
        <!-- Elegant subtle glowing backdrops -->
        <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-luxury-gold/5 rounded-full blur-[120px] pointer-events-none"></div>
        <div class="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-luxury-gold/3 rounded-full blur-[100px] pointer-events-none"></div>

        <div class="max-w-4xl text-center z-10 space-y-8">
            <span class="text-[10px] tracking-[0.4em] uppercase text-luxury-gold font-semibold bg-luxury-gold/10 px-4 py-2 rounded-full border border-luxury-gold/20">
                Estética Avançada de Alto Padrão
            </span>
            
            <h1 class="text-4xl sm:text-6xl font-serif tracking-wide text-white leading-tight">
                Sua beleza esculpida com <br class="hidden sm:inline" />
                <span class="italic text-luxury-gold">precisão e sofisticação</span>
            </h1>
            
            <p class="text-xs sm:text-sm text-gray-400 max-w-xl mx-auto leading-relaxed font-light">
                Combinamos a ciência dermatológica mais avançada a uma abordagem artística exclusiva para revelar a melhor versão da sua expressão facial.
            </p>

            <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
                <a 
                    href={whatsappUrl} 
                    target="_blank"
                    rel="noopener noreferrer"
                    class="w-full sm:w-auto bg-luxury-gold text-luxury-black hover:bg-luxury-gold/90 font-bold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase shadow-lg shadow-luxury-gold/10 hover:scale-[1.02]"
                >
                    Agendar Minha Consulta
                </a>
                <a 
                    href="#procedimentos" 
                    class="w-full sm:w-auto border border-luxury-border hover:border-luxury-gold text-white font-semibold px-8 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase bg-luxury-card/20 hover:bg-luxury-card/40"
                >
                    Conhecer Tratamentos
                </a>
            </div>
        </div>
        
        <!-- Bottom elegant scroll indicator line -->
        <div class="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center space-y-2 opacity-40">
            <span class="text-[9px] tracking-widest uppercase">Descubra</span>
            <div class="w-px h-10 bg-gradient-to-b from-luxury-gold to-transparent"></div>
        </div>
    </section>

    <!-- Procedures Section -->
    <section id="procedimentos" class="py-24 px-6 bg-luxury-dark/45 border-y border-luxury-border/30 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center space-y-3">
                <span class="text-[10px] tracking-widest uppercase text-luxury-gold font-semibold">Tratamentos Exclusivos</span>
                <h2 class="text-3xl font-serif tracking-wide text-luxury-accent">Procedimentos Faciais de Alta Performance</h2>
                <div class="w-12 h-0.5 bg-luxury-gold mx-auto mt-4"></div>
            </div>

            <!-- Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                {#each procedures as proc}
                    <div class="bg-luxury-card border border-luxury-border/50 p-8 rounded-2xl flex flex-col justify-between hover:border-luxury-gold transition duration-300 group">
                        <div class="space-y-4">
                            <div class="flex items-start justify-between">
                                <h3 class="font-serif text-lg text-white group-hover:text-luxury-gold transition duration-200">{proc.name}</h3>
                                <span class="text-xs bg-luxury-black/50 px-3 py-1 rounded border border-luxury-border text-luxury-gold font-mono">{proc.price}</span>
                            </div>
                            <p class="text-xs text-gray-400 leading-relaxed font-light">{proc.desc}</p>
                        </div>
                        <div class="pt-6 mt-6 border-t border-luxury-border/30 flex items-center justify-between text-[11px] text-gray-500 font-mono">
                            <span>Sessão: {proc.duration}</span>
                            <span class="text-luxury-gold font-sans uppercase tracking-wider font-semibold opacity-0 group-hover:opacity-100 transition duration-300">
                                Agendar via WhatsApp →
                            </span>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </section>

    <!-- Boutique Credentials Section -->
    <section class="py-24 px-6 relative overflow-hidden">
        <div class="max-w-4xl mx-auto text-center space-y-12">
            <h2 class="text-3xl font-serif tracking-wide text-luxury-accent">O Padrão Unic Clinic</h2>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
                <div class="space-y-3 p-4">
                    <div class="text-2xl text-luxury-gold font-serif">I</div>
                    <h4 class="text-xs tracking-wider uppercase font-semibold text-white">Atendimento Boutique</h4>
                    <p class="text-xs text-gray-400 font-light leading-relaxed">Experiência altamente personalizada e exclusiva com privacidade garantida do início ao fim.</p>
                </div>
                <div class="space-y-3 p-4">
                    <div class="text-2xl text-luxury-gold font-serif">II</div>
                    <h4 class="text-xs tracking-wider uppercase font-semibold text-white">Tecnologia Médica</h4>
                    <p class="text-xs text-gray-400 font-light leading-relaxed">Portfólio com os melhores produtos e injetáveis do mercado mundial, certificados pela ANVISA.</p>
                </div>
                <div class="space-y-3 p-4">
                    <div class="text-2xl text-luxury-gold font-serif">III</div>
                    <h4 class="text-xs tracking-wider uppercase font-semibold text-white">Equipe Especializada</h4>
                    <p class="text-xs text-gray-400 font-light leading-relaxed">Profissionais pós-graduados dedicados à beleza natural e harmonização facial sutil.</p>
                </div>
            </div>

            <div class="pt-8">
                <a 
                    href={whatsappUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-block bg-transparent border border-luxury-gold text-luxury-gold hover:bg-luxury-gold hover:text-luxury-black font-bold px-10 py-4 rounded transition-all duration-300 text-xs tracking-widest uppercase"
                >
                    Falar com um Especialista
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 px-6 border-t border-luxury-border/30 bg-luxury-dark/80 text-center text-xs text-gray-500 space-y-4">
        <p class="font-serif tracking-[0.2em] text-luxury-gold uppercase text-sm">UNIC CLINIC</p>
        <p class="max-w-md mx-auto font-light leading-relaxed">São Paulo - SP | Atendimento exclusivo com hora marcada.</p>
        <p class="text-[10px] opacity-50">&copy; 2026 Unic Clinic. Todos os direitos reservados.</p>
    </footer>
</div>
