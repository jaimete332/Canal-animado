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

## Programar la publicación a una hora

YouTube publica el vídeo solo a la hora indicada (no hace falta tener el ordenador encendido): se sube
ya como privado con `publishAt` y la miniatura de `thumbnail.png`.

```bash
python -m fabrica approve ceniza-de-volcan
python -m fabrica upload ceniza-de-volcan --at "2026-11-21 18:00"        # hora de youtube.timezone (Europe/Madrid)

# varios de una vez (valida todas las fechas antes de subir nada):
python -m fabrica schedule ceniza-de-volcan="2026-11-21 18:00" sin-casco-en-el-espacio="2026-11-23 18:00" \
                           agua-helada-del-titanic="2026-11-25 18:00"
python -m fabrica schedule ... --dry-run   # comprueba aprobaciones y fechas sin subir nada
```

* Sirve tanto `output/<slug>/` como `samples/<slug>/` (en otra máquina basta con `git pull`).
* La hora debe estar al menos 15 minutos en el futuro. Cambia la zona en `config.yaml` → `youtube.timezone`.
* La miniatura personalizada exige que el canal esté verificado por teléfono (youtube.com/verify).
* **Proyecto de Google sin verificar**: YouTube bloquea como privados los vídeos subidos por API desde
  proyectos que no han pasado la auditoría, y entonces la publicación programada no llega a hacerse
  pública. Solicita la auditoría (formulario «YouTube API Services - Audit and Quota Extension») o, mientras
  tanto, sube con `upload` y programa la hora tú en YouTube Studio → Visibilidad → Programar.

Notas:
* Cuota: subir un vídeo cuesta 1.600 unidades de las 10.000 diarias (~6 vídeos/día).
* Los proyectos de Google no verificados suben vídeos como privados hasta pasar la auditoría de la API:
  para automatizar publicaciones públicas solicita la verificación (o publica tú desde Studio).
* Se marca `containsSyntheticMedia: true` (voz sintética), tal y como exige la política de YouTube.
* Métricas: `python -m fabrica metrics` (requiere el mismo OAuth) → `python -m fabrica insights`.
