# Quickstart: Landing Page Atanazio Modas

## Visualização Local

A landing page é concebida como um artefato web moderno e autossuficiente (Zero Build Step), facilitando testes e deploy imediato:

### Opção 1: Abrir diretamente no navegador
```bash
# No Windows PowerShell:
Start-Process "atanazio_modas/atanazio-modas.html"
```

### Opção 2: Servidor estático local (Python ou Node)
```bash
# Via Python:
python -m http.server 8080 --directory atanazio_modas

# Acesse no navegador:
http://localhost:8080/atanazio-modas.html
```

---

## Verificação de Rastreamento (Console do Desenvolvedor)

1. Abra o DevTools (`F12` ou `Ctrl+Shift+I`) e vá para a aba **Console**.
2. Clique no botão de CTA do Hero, no botão do Header ou no botão flutuante do WhatsApp.
3. Observe os logs de depuração:
   ```javascript
   [DataLayer] conversion_intent: lead_whatsapp_hero { category: 'WhatsApp', id: 'btn-hero-wa' }
   ```
4. Verifique o array global no console:
   ```javascript
   console.table(window.dataLayer)
   ```

---

## Publicação / Deploy

1. **Deploy Estático**: Os arquivos da pasta `atanazio_modas/` podem ser sincronizados para qualquer bucket S3, Cloudflare Pages, Vercel ou Nginx estático.
2. **Integração com GTM / Meta Pixel**:
   - Para adicionar o container GTM, basta injetar a tag `<script>` padrão do GTM no `<head>` de `index.html`. O script de dataLayer nativo já está sincronizado e disparará as tags sem necessidade de alterações no DOM.
