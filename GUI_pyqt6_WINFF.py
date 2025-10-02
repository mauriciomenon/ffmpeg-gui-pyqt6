# GUI_pyqt6_WINFF.py
# Conversão da interface Tkinter para PyQt6

import os
import sys
import subprocess
import json
import platform
import threading
import webbrowser
import tempfile
import zipfile
from io import BytesIO
from functools import partial

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFileDialog, QCheckBox, QHBoxLayout, QVBoxLayout

class FFmpegGuiPyQt6(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Conversor de Vídeo Avançado (PyQt6)')
        self.resize(900, 700)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # top buttons
        top_layout = QHBoxLayout()
        about_btn = QPushButton('About')
        about_btn.clicked.connect(self.show_about)
        info_btn = QPushButton('Informações do video')
        info_btn.clicked.connect(self.show_video_info)
        dl_btn = QPushButton('Baixar FFmpeg')
        dl_btn.clicked.connect(self.download_ffmpeg_and_maybe_install)
        top_layout.addWidget(about_btn)
        top_layout.addStretch()
        top_layout.addWidget(info_btn)
        top_layout.addWidget(dl_btn)
        layout.addLayout(top_layout)

        # input file
        h = QHBoxLayout()
        h.addWidget(QLabel('Selecione o Arquivo de Vídeo:'))
        self.input_edit = QLineEdit()
        self.input_edit.textChanged.connect(self.update_command_display)
        h.addWidget(self.input_edit)
        browse_btn = QPushButton('Procurar')
        browse_btn.clicked.connect(self.select_file)
        h.addWidget(browse_btn)
        layout.addLayout(h)

        # output dir
        h = QHBoxLayout()
        h.addWidget(QLabel('Selecione o Diretório de Saída:'))
        self.output_edit = QLineEdit()
        self.output_edit.textChanged.connect(self.update_command_display)
        h.addWidget(self.output_edit)
        out_browse = QPushButton('Procurar')
        out_browse.clicked.connect(self.select_output_directory)
        h.addWidget(out_browse)
        layout.addLayout(h)

        # same dir checkbox / overwrite
        h = QHBoxLayout()
        self.same_dir_chk = QCheckBox('Utilizar o mesmo diretório do arquivo de entrada')
        self.same_dir_chk.stateChanged.connect(self.toggle_output_dir)
        h.addWidget(self.same_dir_chk)
        self.overwrite_chk = QCheckBox('Sobrescrever arquivos existentes')
        self.overwrite_chk.setChecked(True)
        h.addWidget(self.overwrite_chk)
        layout.addLayout(h)

        # format + codecs
        grid = QtWidgets.QGridLayout()
        grid.addWidget(QLabel('Formato de Saída:'), 0, 0)
        self.format_combo = QComboBox(); self.format_combo.addItems(['mp4','avi','mkv','flv','mov','mp3','wmv','asf'])
        self.format_combo.currentIndexChanged.connect(self.update_command_display)
        grid.addWidget(self.format_combo, 0, 1)

        grid.addWidget(QLabel('Codec de Vídeo:'), 1, 0)
        self.video_codec_combo = QComboBox(); self.video_codec_combo.addItems(['auto','libx264','libx265','mpeg4','wmv2'])
        self.video_codec_combo.currentIndexChanged.connect(self.update_command_display)
        grid.addWidget(self.video_codec_combo, 1, 1)

        grid.addWidget(QLabel('Codec de Áudio:'), 2, 0)
        self.audio_codec_combo = QComboBox(); self.audio_codec_combo.addItems(['auto','aac','mp3','ac3','wmav2'])
        self.audio_codec_combo.currentIndexChanged.connect(self.update_command_display)
        grid.addWidget(self.audio_codec_combo, 2, 1)

        grid.addWidget(QLabel('Resolução:'), 3, 0)
        self.resolution_combo = QComboBox(); self.resolution_combo.addItems(['original','1920x1080','1280x720','640x480','320x240'])
        self.resolution_combo.currentIndexChanged.connect(self.update_command_display)
        grid.addWidget(self.resolution_combo, 3, 1)

        grid.addWidget(QLabel('Bitrate de Vídeo:'), 4, 0)
        self.video_bitrate = QLineEdit(); self.video_bitrate.textChanged.connect(self.update_command_display)
        grid.addWidget(self.video_bitrate, 4, 1)

        grid.addWidget(QLabel('Bitrate de Áudio:'), 5, 0)
        self.audio_bitrate = QLineEdit(); self.audio_bitrate.textChanged.connect(self.update_command_display)
        grid.addWidget(self.audio_bitrate, 5, 1)

        grid.addWidget(QLabel('FPS (frame rate):'), 6, 0)
        self.frame_rate = QLineEdit(); self.frame_rate.textChanged.connect(self.update_command_display)
        grid.addWidget(self.frame_rate, 6, 1)

        grid.addWidget(QLabel('Audio sample rate:'), 7, 0)
        self.audio_sample_rate = QLineEdit(); self.audio_sample_rate.textChanged.connect(self.update_command_display)
        grid.addWidget(self.audio_sample_rate, 7, 1)

        grid.addWidget(QLabel('Audio channels:'), 8, 0)
        self.audio_channels = QComboBox(); self.audio_channels.addItems(['1','2'])
        self.audio_channels.currentIndexChanged.connect(self.update_command_display)
        grid.addWidget(self.audio_channels, 8, 1)

        # no-audio checkbox positioned near audio controls
        no_audio_row = QHBoxLayout()
        self.no_audio_chk = QCheckBox('Arquivo sem áudio (-an)')
        self.no_audio_chk.stateChanged.connect(self.on_no_audio_change)
        no_audio_row.addWidget(self.no_audio_chk)
        grid.addLayout(no_audio_row, 9, 0, 1, 2)

        layout.addLayout(grid)

        # ffmpeg path
        h = QHBoxLayout()
        h.addWidget(QLabel('Caminho do Executável FFmpeg:'))
        self.ffmpeg_path = QLineEdit()
        self.ffmpeg_path.setText('ffmpeg')
        self.ffmpeg_path.textChanged.connect(self.update_command_display)
        h.addWidget(self.ffmpeg_path)
        ff_browse = QPushButton('Procurar')
        ff_browse.clicked.connect(self.select_ffmpeg)
        h.addWidget(ff_browse)
        layout.addLayout(h)

        # command display
        layout.addWidget(QLabel('Comando FFmpeg:'))
        self.command_display = QTextEdit(); self.command_display.setReadOnly(True)
        layout.addWidget(self.command_display)

        # buttons
        btn_layout = QHBoxLayout()
        default_btn = QPushButton('Opções Padrão'); default_btn.clicked.connect(self.set_default_options)
        btn_layout.addWidget(default_btn)
        load_btn = QPushButton('Carregar Configuração'); load_btn.clicked.connect(self.load_config)
        btn_layout.addWidget(load_btn)
        save_btn = QPushButton('Salvar Configuração'); save_btn.clicked.connect(self.save_config)
        btn_layout.addWidget(save_btn)
        convert_btn = QPushButton('Converter'); convert_btn.clicked.connect(self.convert_video)
        btn_layout.addWidget(convert_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.set_default_options()

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Selecione o arquivo de vídeo')
        if file:
            self.input_edit.setText(file)

    def select_output_directory(self):
        d = QFileDialog.getExistingDirectory(self, 'Selecione o diretório de saída')
        if d:
            self.output_edit.setText(d)

    def toggle_output_dir(self):
        if self.same_dir_chk.isChecked():
            self.output_edit.setDisabled(True)
        else:
            self.output_edit.setDisabled(False)
        self.update_command_display()

    def select_ffmpeg(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Selecione o FFmpeg')
        if file:
            self.ffmpeg_path.setText(file)

    def set_default_options(self):
        self.format_combo.setCurrentText('wmv')
        self.resolution_combo.setCurrentText('original')
        self.video_codec_combo.setCurrentText('wmv2')
        self.audio_codec_combo.setCurrentText('wmav2')
        self.video_bitrate.setText('204800')
        self.audio_bitrate.setText('65536')
        self.frame_rate.setText('20')
        self.audio_sample_rate.setText('22050')
        self.audio_channels.setCurrentText('1')
        self.output_edit.clear()
        self.ffmpeg_path.setText('ffmpeg')
        self.same_dir_chk.setChecked(False)
        self.overwrite_chk.setChecked(True)
        self.no_audio_chk.setChecked(False)
        self.update_command_display()

    def load_config(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Carregar Configuração', filter='INI Files (*.ini)')
        if not file:
            return
        import configparser
        cp = configparser.ConfigParser(); cp.read(file)
        d = cp['DEFAULT'] if 'DEFAULT' in cp else {}
        self.ffmpeg_path.setText(d.get('ffmpeg_path','ffmpeg'))
        self.format_combo.setCurrentText(d.get('default_format','wmv'))
        self.output_edit.setText(d.get('default_output_dir',''))
        self.video_codec_combo.setCurrentText(d.get('default_video_codec','wmv2'))
        self.audio_codec_combo.setCurrentText(d.get('default_audio_codec','wmav2'))
        self.resolution_combo.setCurrentText(d.get('default_resolution','original'))
        self.video_bitrate.setText(d.get('video_bitrate','204800'))
        self.audio_bitrate.setText(d.get('audio_bitrate','65536'))
        self.frame_rate.setText(d.get('frame_rate','20'))
        self.audio_sample_rate.setText(d.get('audio_sample_rate','22050'))
        self.audio_channels.setCurrentText(d.get('audio_channels','1'))
        self.same_dir_chk.setChecked(d.get('use_same_directory','False')=='True')
        self.overwrite_chk.setChecked(d.get('overwrite_existing','True')=='True')
        self.no_audio_chk.setChecked(d.get('no_audio','False')=='True')
        self.on_no_audio_change()  # apply UI disable state
        self.update_command_display()

    def save_config(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Salvar Configuração', filter='INI Files (*.ini)')
        if not file:
            return
        import configparser
        cp = configparser.ConfigParser()
        cp['DEFAULT'] = {
            'ffmpeg_path': self.ffmpeg_path.text(),
            'default_format': self.format_combo.currentText(),
            'default_output_dir': self.output_edit.text(),
            'default_video_codec': self.video_codec_combo.currentText(),
            'default_audio_codec': self.audio_codec_combo.currentText(),
            'default_resolution': self.resolution_combo.currentText(),
            'video_bitrate': self.video_bitrate.text(),
            'audio_bitrate': self.audio_bitrate.text(),
            'frame_rate': self.frame_rate.text(),
            'audio_sample_rate': self.audio_sample_rate.text(),
            'audio_channels': self.audio_channels.currentText(),
            'use_same_directory': str(self.same_dir_chk.isChecked()),
            'overwrite_existing': str(self.overwrite_chk.isChecked()),
            'no_audio': str(self.no_audio_chk.isChecked()),
        }
        with open(file, 'w') as f:
            cp.write(f)

    def build_command(self):
        inp = self.input_edit.text()
        fmt = self.format_combo.currentText()
        video_bitrate = self.video_bitrate.text()
        audio_bitrate = self.audio_bitrate.text()
        resolution = self.resolution_combo.currentText()
        video_codec = self.video_codec_combo.currentText()
        audio_codec = self.audio_codec_combo.currentText()
        frame_rate = self.frame_rate.text()
        audio_sample_rate = self.audio_sample_rate.text()
        audio_channels = self.audio_channels.currentText()
        ffmpeg = self.ffmpeg_path.text()

        if self.same_dir_chk.isChecked():
            out_dir = os.path.dirname(inp)
        else:
            out_dir = self.output_edit.text()
        output_file = os.path.join(out_dir, os.path.splitext(os.path.basename(inp))[0] + '.' + fmt) if inp else ''

        cmd = f'"{ffmpeg}" -y -i "{inp}"' if inp else ''
        if video_bitrate:
            cmd += f' -b:v {video_bitrate}'
        if self.no_audio_chk.isChecked():
            cmd += ' -an'
        elif audio_bitrate:
            cmd += f' -b:a {audio_bitrate}'
        if resolution != 'original':
            cmd += f' -s {resolution}'
        if frame_rate:
            cmd += f' -r {frame_rate}'
        if not self.no_audio_chk.isChecked() and audio_sample_rate:
            cmd += f' -ar {audio_sample_rate}'
        if not self.no_audio_chk.isChecked() and audio_channels:
            cmd += f' -ac {audio_channels}'
        if video_codec != 'auto':
            cmd += f' -vcodec {video_codec}'
        if not self.no_audio_chk.isChecked() and audio_codec != 'auto':
            cmd += f' -acodec {audio_codec}'
        if output_file:
            cmd += f' "{output_file}"'
        return cmd

    def update_command_display(self):
        cmd = self.build_command()
        self.command_display.setPlainText(cmd)

    def convert_video(self):
        cmd = self.build_command()
        if not cmd:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Preencha os campos necessários')
            return
        try:
            subprocess.run(cmd, shell=True, check=True)
            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Vídeo convertido com sucesso!')
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Falha ao converter vídeo.\nErro: {e}')

    def show_about(self):
        QtWidgets.QMessageBox.information(self, 'About', 'Mauricio Menon (+AI)\nhttps://github.com/mauriciomenon\nPyQt6 version of the GUI')

    def show_video_info(self):
        inp = self.input_edit.text()
        if not inp:
            QtWidgets.QMessageBox.warning(self, 'Atenção', 'Nenhum arquivo selecionado')
            return
        ffprobe = os.path.join(os.path.dirname(self.ffmpeg_path.text()), 'ffprobe.exe' if os.name == 'nt' else 'ffprobe')
        if not os.path.exists(ffprobe):
            QtWidgets.QMessageBox.critical(self, 'Erro', 'ffprobe não encontrado no caminho do ffmpeg')
            return
        try:
            command = [ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', inp]
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                raise RuntimeError('ffprobe error')
            data = json.loads(out)
            info_text = json.dumps(data, indent=2, ensure_ascii=False)
            dlg = QtWidgets.QDialog(self)
            dlg.setWindowTitle('Informações detalhadas do vídeo')
            v = QVBoxLayout()
            te = QTextEdit(); te.setPlainText(info_text); te.setReadOnly(True)
            v.addWidget(te)
            b = QPushButton('Fechar'); b.clicked.connect(dlg.accept)
            v.addWidget(b)
            dlg.setLayout(v)
            dlg.exec()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Falha ao obter info: {e}')

    def on_no_audio_change(self):
        disabled = self.no_audio_chk.isChecked()
        self.audio_codec_combo.setDisabled(disabled)
        self.audio_bitrate.setDisabled(disabled)
        self.audio_sample_rate.setDisabled(disabled)
        self.audio_channels.setDisabled(disabled)
        self.update_command_display()

    # -------- FFmpeg download helpers --------
    def _get_latest_ffmpeg_windows_zip_url(self):
        # Try GitHub API (BtbN/FFmpeg-Builds) for latest win64 gpl zip; fallback to a known asset name
        try:
            import requests
            api = 'https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest'
            resp = requests.get(api, timeout=10)
            if resp.ok:
                data = resp.json()
                for asset in data.get('assets', []):
                    name = asset.get('name','')
                    if name.endswith('win64-gpl.zip'):
                        return asset.get('browser_download_url')
        except Exception:
            pass
        # Fallback to latest/download with a common asset name
        return 'https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip'

    def _extract_ffmpeg_zip(self, zip_bytes):
        # Extract to ./bin and return inferred ffmpeg path
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin'))
        os.makedirs(base_dir, exist_ok=True)
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
            zf.extractall(base_dir)
        # try to find ffmpeg(.exe)
        ffmpeg_path = None
        for root, dirs, files in os.walk(base_dir):
            for f in files:
                if f.lower() == ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'):
                    ffmpeg_path = os.path.join(root, f)
                    break
            if ffmpeg_path:
                break
        return ffmpeg_path

    def download_ffmpeg_and_maybe_install(self):
        # On non-Windows, open releases page; on Windows, download and extract
        if platform.system() != 'Windows':
            webbrowser.open('https://github.com/BtbN/FFmpeg-Builds/releases')
            QtWidgets.QMessageBox.information(self, 'FFmpeg', 'Em sistemas não Windows, abrimos a página de releases para download manual.')
            return

        def worker():
            try:
                import requests
                url = self._get_latest_ffmpeg_windows_zip_url()
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                ff = self._extract_ffmpeg_zip(r.content)
                if ff:
                    # Update UI on main thread
                    QtCore.QMetaObject.invokeMethod(
                        self.ffmpeg_path, 'setText', QtCore.Qt.ConnectionType.QueuedConnection, QtCore.Q_ARG(str, ff)
                    )
                    QtCore.QMetaObject.invokeMethod(
                        self, 'show_info_msg', QtCore.Qt.ConnectionType.QueuedConnection,
                        QtCore.Q_ARG(str, 'FFmpeg baixado e extraído com sucesso.')
                    )
                else:
                    QtCore.QMetaObject.invokeMethod(
                        self, 'show_error_msg', QtCore.Qt.ConnectionType.QueuedConnection,
                        QtCore.Q_ARG(str, 'Não foi possível localizar o executável ffmpeg após extração.')
                    )
            except Exception as e:
                QtCore.QMetaObject.invokeMethod(
                    self, 'show_error_msg', QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, f'Falha no download: {e}')
                )

        threading.Thread(target=worker, daemon=True).start()

    @QtCore.pyqtSlot(str)
    def show_info_msg(self, msg):
        QtWidgets.QMessageBox.information(self, 'Info', msg)

    @QtCore.pyqtSlot(str)
    def show_error_msg(self, msg):
        QtWidgets.QMessageBox.critical(self, 'Erro', msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FFmpegGuiPyQt6()
    w.show()
    sys.exit(app.exec())
