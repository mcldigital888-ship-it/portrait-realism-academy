# Stack: GitHub → OVH → Cloudflare

**GitHub (fabbrica)** — codice + CI. Repo `mcldigital888-ship-it/portrait-realism-academy`, branch `main`.
**OVH (negozio)** — VPS Ubuntu che serve il sito (nginx). È dove "gira" materialmente.
**Cloudflare (corriere + security)** — davanti a OVH: CDN, cache, WAF/anti-DDoS, HTTPS.

## Flusso
`git push main` → GitHub Actions (`.github/workflows/deploy-ovh.yml`) rsync-a i file sul VPS OVH → Cloudflare (proxied) serve e protegge.
_(Alternativa consigliata dal piano migrazione: **Coolify** installato sul VPS OVH, connesso a GitHub, che auto-builda e deploya ad ogni push — sostituisce il workflow Actions.)_

## Cosa serve per attivarlo (da fornire)
1. **VPS OVH**: IP pubblico + accesso `root`/utente SSH (o token API OVH per crearlo). Consigliato dal piano: VPS "Value/Elite", Ubuntu 24.04, area Milano.
2. **Cloudflare**: account + dominio `portraitrealismacademy.com` aggiunto (cambio nameserver ai CF) + **API token** (Zone.DNS edit) per automatizzare i record.
3. Sul VPS: eseguire `deploy/ovh-bootstrap.sh portraitrealismacademy.com`.
4. Su GitHub: secrets `OVH_HOST`, `OVH_USER`, `OVH_SSH_KEY`, `OVH_PATH=/var/www/academy` + variabile `OVH_ENABLED=true`.

## Stato attuale (2026-07-12)
Sito LIVE in via provvisoria su **GitHub Pages** (statico, HTTPS, CDN Fastly) su portraitrealismacademy.com. Si migra su OVH+Cloudflare appena il VPS è pronto: allora si sposta il record DNS del dominio su Cloudflare → IP OVH e si spegne Pages.

## Nota di merito
Per un sito **statico** (questa landing), GitHub Pages basta e avanza. OVH (CPU/RAM) diventa necessario per le parti **dinamiche**: backend acconti/pagamenti, CRM, bot AI lead. Lo stack OVH+Cloudflare è il posto giusto per quelle + come standard unico dell'ecosistema.
