# Clip del «humano real» para el anuncio Blowfish

El anuncio ya está terminado usando las fotos reales de la sudadera. Si quieres que en el mundo real
aparezca **una persona real hablando**, graba este clip y la fábrica lo integra sola: dentro del espejo
y a pantalla completa, con su propia voz y subtítulos sincronizados.

## Qué decir (≈5 segundos, con energía y sonriendo a cámara)
> «¡Hola, Leo! Bienvenido al mundo real. Aquí tu sudadera existe de verdad.»

Si cambias la frase, cambia también el texto de la escena `b07` en `scripts/story_blowfish.py`
(los subtítulos salen de ahí).

## Cómo grabarlo
* **Vertical** (9:16), el móvil vale. Persona de cintura para arriba, centrada, **con la sudadera puesta**.
* Que se vea el logo del pecho. Si puede, al final que se gire un segundo para enseñar la espalda.
* Luz de frente (una ventana), fondo limpio y claro (gris o blanco va genial con las fotos del producto).
* Sin música de fondo; habla cerca del móvil. Deja 0,5 s de silencio al principio y al final.
* Duración: entre 4 y 7 segundos.
* La persona debe dar su **consentimiento** para aparecer en el anuncio.

## Cómo añadirlo
1. Guarda el vídeo como `assets/blowfish/humano.mp4` (o pásamelo por aquí y lo coloco yo).
2. Ejecuta:
   ```bash
   python3 scripts/story_blowfish.py
   python -m fabrica make stories/anuncio-blowfish.json
   ```
3. Resultado en `output/anuncio-blowfish/final.mp4`.
