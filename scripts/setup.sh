#!/usr/bin/env bash
# Instalación completa: dependencias del sistema, Python y modelos locales (~850 MB).
set -euo pipefail
cd "$(dirname "$0")/.."

if command -v apt-get >/dev/null; then
  sudo apt-get update && sudo apt-get install -y ffmpeg libcairo2-dev pkg-config python3-dev fontconfig
elif command -v brew >/dev/null; then
  brew install ffmpeg cairo pkg-config
fi

python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

mkdir -p models/kokoro
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f models/kokoro/kokoro-v1.0.onnx ] || curl -L -o models/kokoro/kokoro-v1.0.onnx $K/kokoro-v1.0.onnx
[ -f models/kokoro/voices-v1.0.bin ]  || curl -L -o models/kokoro/voices-v1.0.bin  $K/voices-v1.0.bin

S=https://github.com/k2-fsa/sherpa-onnx/releases/download
if [ ! -d models/vits-piper-es_ES-davefx-medium ]; then
  curl -L $S/tts-models/vits-piper-es_ES-davefx-medium.tar.bz2 | tar xj -C models
  curl -L $S/tts-models/vits-piper-es_ES-sharvard-medium.tar.bz2 | tar xj -C models
fi
if [ ! -d models/whisper-small ]; then
  curl -L $S/asr-models/sherpa-onnx-whisper-small.tar.bz2 | tar xj -C models
  mv models/sherpa-onnx-whisper-small models/whisper-small
  rm -f models/whisper-small/small-encoder.onnx models/whisper-small/small-decoder.onnx
  rm -rf models/whisper-small/test_wavs
fi

[ -f .env ] || cp .env.example .env
python -m fabrica doctor
echo "Listo. Prueba: python -m fabrica make stories/centro-de-la-tierra.json"
