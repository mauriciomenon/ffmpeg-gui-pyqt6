# GUI_pyqt6_WINFF.py
# Conversão da interface Tkinter para PyQt6

import os
import sys
import subprocess
import json
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
        top_layout.addWidget(about_btn)
        top_layout.addStretch()
        top_layout.addWidget(info_btn)
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
        self.format_combo = QComboBox(); self.format_combo.addItems(['mp4','avi','mkv','flv','mov','mp3','wmv'])
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
        self.resolution_combo.setCurrentText('320x240')
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
        self.resolution_combo.setCurrentText(d.get('default_resolution','320x240'))
        self.video_bitrate.setText(d.get('video_bitrate','204800'))
        self.audio_bitrate.setText(d.get('audio_bitrate','65536'))
        self.frame_rate.setText(d.get('frame_rate','20'))
        self.audio_sample_rate.setText(d.get('audio_sample_rate','22050'))
        self.audio_channels.setCurrentText(d.get('audio_channels','1'))
        self.same_dir_chk.setChecked(d.get('use_same_directory','False')=='True')
        self.overwrite_chk.setChecked(d.get('overwrite_existing','True')=='True')
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
            'overwrite_existing': str(self.overwrite_chk.isChecked())
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
        if audio_bitrate:
            cmd += f' -b:a {audio_bitrate}'
        if resolution != 'original':
            cmd += f' -s {resolution}'
        if frame_rate:
            cmd += f' -r {frame_rate}'
        if audio_sample_rate:
            cmd += f' -ar {audio_sample_rate}'
        if audio_channels:
            cmd += f' -ac {audio_channels}'
        if video_codec != 'auto':
            cmd += f' -vcodec {video_codec}'
        if audio_codec != 'auto':
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FFmpegGuiPyQt6()
    w.show()
    sys.exit(app.exec())
