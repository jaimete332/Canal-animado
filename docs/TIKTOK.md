# Publicación en TikTok (opcional, con aprobación)

La fábrica usa la **Content Posting API oficial de TikTok**. Nunca se usan tu usuario ni tu contraseña:
autorizas la cuenta con el inicio de sesión oficial de TikTok y se guarda un token en `secrets/` (fuera de git).

## 1. Crear la app de desarrollador (una vez, ~15 min)
1. Entra en **developers.tiktok.com** con tu cuenta de TikTok → *Manage apps* → **Connect an app**.
2. Rellena nombre («Hipotéticos Uploader»), icono (`assets/branding/profile.png`), categoría y descripción.
   Te pedirá URL de términos y de privacidad: puedes usar páginas sencillas (p. ej. en GitHub Pages).
3. Añade los productos **Login Kit** y **Content Posting API**.
   * En Content Posting API activa **Direct Post** (y deja también la subida a borradores).
4. Scopes: `user.info.basic`, `video.upload`, `video.publish`.
5. Plataforma **Desktop** y *Redirect URI*: `http://localhost:8765/callback/`
6. Copia **Client key** y **Client secret** a tu `.env`:
   ```
   TIKTOK_CLIENT_KEY=...
   TIKTOK_CLIENT_SECRET=...
   ```
7. En el *Sandbox* de la app, añade tu cuenta de TikTok como **Target user** para poder probar.

## 2. Autorizar tu cuenta (en tu ordenador)
```bash
python -m fabrica tiktok-auth      # se abre el navegador → aceptas → «Listo»
```
Este paso necesita un navegador, así que hazlo en tu ordenador (no en la sesión en la nube).
Después puedes copiar `secrets/tiktok_token.json` a donde ejecutes la fábrica; se renueva solo.

## 3. Publicar
En `config.yaml`: `tiktok.enabled: true`. Luego:
```bash
python -m fabrica approve centro-de-la-tierra              # tu aprobación (la misma que para YouTube)
python -m fabrica tiktok-upload centro-de-la-tierra --draft  # → a tus borradores de la app de TikTok
python -m fabrica tiktok-upload centro-de-la-tierra          # → publicación directa
```
El texto del post se genera solo (título + gancho + pregunta + hashtags) y se marca como
**contenido generado con IA**, como exige TikTok.

## Limitaciones importantes de TikTok
* **Apps sin auditar = solo privado.** Hasta que TikTok apruebe tu app (*Audit* en el portal, suele tardar
  días o semanas), los vídeos con publicación directa solo pueden subirse con visibilidad **«Solo yo»**
  (`SELF_ONLY`). Después de la auditoría podrás usar `--privacy PUBLIC_TO_EVERYONE`.
* **Alternativa inmediata: `--draft`.** Envía el vídeo a la bandeja de borradores de tu app de TikTok;
  desde el móvil eliges portada o sonido y le das a publicar. Es la forma más rápida de empezar.
* Límite de publicaciones diarias por cuenta según TikTok (consulta *creator_info* en el portal).
* La miniatura de TikTok se elige como fotograma del vídeo (`tiktok.cover_ms`).
* Red: el entorno que suba los vídeos debe poder conectar con `open.tiktokapis.com`.
