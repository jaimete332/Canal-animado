# API keys: cuáles hacen falta y cómo conseguirlas

Ninguna es obligatoria para producir vídeos desde un guion JSON. Se configuran en `.env` (copia de `.env.example`).

| Para qué | Variable | Dónde conseguirla | Coste aprox. |
|---|---|---|---|
| Guiones automáticos (recomendado) | `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys | ~0,05-0,10 $/guion |
| Alternativa | `OPENAI_API_KEY` | platform.openai.com → API keys | ~0,01-0,05 $/guion |
| Alternativa (con capa gratuita) | `GEMINI_API_KEY` | aistudio.google.com → Get API key | 0-0,02 $/guion |
| Voz premium | `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID` | elevenlabs.io → Profile → API key; Voice Library → voz «Spanish (Spain)» → copiar ID | ~0,15-0,20 $/vídeo |
| Voz Google | `GOOGLE_TTS_API_KEY` | console.cloud.google.com → habilitar Text-to-Speech → Credenciales | ~0,03 $/vídeo |
| Fondos IA | `OPENAI_API_KEY` / `GEMINI_API_KEY` / `REPLICATE_API_TOKEN` | replicate.com → Account → API tokens | 0,003-0,04 $/imagen |

Después de añadir una clave:

```bash
python -m fabrica doctor           # debe mostrar 🔑 configurada
```

Y en `config.yaml`:
* `llm.provider: auto` usa la primera clave disponible.
* Voz: `tts.provider: elevenlabs` (o `edge`, gratis, si tu red permite `speech.platform.bing.com`).
* Fondos IA: `images.provider: gemini` y añade `"image_prompt": "..."` en las escenas que quieras.
