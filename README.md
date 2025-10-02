# ffmpeg-gui-pyqt6

Contém:

- `GUI_tkinter_WINFF.py` — Versão Tkinter (completa) copiada/adaptada do repositório original (Mauricio Menon).
- `GUI_pyqt6_WINFF.py` — Conversão funcional da GUI para PyQt6 (mesmas opções principais: seleção de arquivo, diretório de saída, codecs, bitrate, resolução, preview do comando FFmpeg, execução da conversão, exibir info via ffprobe).
- `requirements.txt` — Dependências sugeridas.

Como testar (macOS / zsh)

1) Criar e ativar um virtualenv (opcional):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Instalar dependências:

```bash
python -m pip install -r requirements.txt
```

3) Executar a GUI PyQt6:

```bash
python GUI_pyqt6_WINFF.py
```

4) Ou executar a GUI Tkinter:

```bash
python GUI_tkinter_WINFF.py
```
