# Publicación en YouTube (opcional, con aprobación)

1. **Google Cloud**: console.cloud.google.com → crea un proyecto → *APIs y servicios* → habilita
   **YouTube Data API v3** y **YouTube Analytics API**.
2. *Pantalla de consentimiento OAuth*: tipo «Externo», añade tu cuenta como usuario de prueba.
3. *Credenciales → Crear credenciales → ID de cliente OAuth → Aplicación de escritorio* → descarga el JSON
   y guárdalo como `secrets/client_secret.json` (carpeta ignorada por git).
4. En `config.yaml`: `youtube.enabled: true` (privacidad por defecto `private`).
5. Flujo:
   ```bash
   python -m fabrica make stories/mi-video.json   # revisa output/mi-video/final.mp4 y qa/report.md
   python -m fabrica approve mi-video             # tu aprobación (firma el hash del vídeo)
   python -m fabrica upload mi-video              # la 1ª vez abre el navegador para autorizar
   ```
6. El comentario se publica automáticamente; **fíjalo** desde YouTube Studio (la API no permite fijarlo).

Notas:
* Cuota: subir un vídeo cuesta 1.600 unidades de las 10.000 diarias (~6 vídeos/día).
* Los proyectos de Google no verificados suben vídeos como privados hasta pasar la auditoría de la API:
  para automatizar publicaciones públicas solicita la verificación (o publica tú desde Studio).
* Se marca `containsSyntheticMedia: true` (voz sintética), tal y como exige la política de YouTube.
* Métricas: `python -m fabrica metrics` (requiere el mismo OAuth) → `python -m fabrica insights`.
