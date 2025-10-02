from importlib import import_module
import sys
import types


def _stub_pyqt6():
    if 'PyQt6' in sys.modules:
        return
    qt = types.ModuleType('PyQt6')
    qtwidgets = types.ModuleType('PyQt6.QtWidgets')
    qtcore = types.ModuleType('PyQt6.QtCore')
    # Provide dummy classes used in import statements
    for name in [
        'QApplication','QWidget','QLabel','QLineEdit','QPushButton','QTextEdit',
        'QComboBox','QFileDialog','QCheckBox','QHBoxLayout','QVBoxLayout','QProgressDialog'
    ]:
        setattr(qtwidgets, name, type(name, (), {}))
    # Minimal decorator used in the module (@QtCore.pyqtSlot)
    qtcore.pyqtSlot = lambda *args, **kwargs: (lambda f: f)
    qt.QtWidgets = qtwidgets
    qt.QtCore = qtcore
    sys.modules['PyQt6'] = qt
    sys.modules['PyQt6.QtWidgets'] = qtwidgets
    sys.modules['PyQt6.QtCore'] = qtcore


def _stub_tkinter():
    if 'tkinter' in sys.modules:
        return
    tk = types.ModuleType('tkinter')
    # Minimal Tk class to support class definition inheritance
    tk.Tk = type('Tk', (), {})
    ttk = types.ModuleType('ttk')
    filedialog = types.ModuleType('filedialog')
    messagebox = types.ModuleType('messagebox')
    # Expose submodules as attributes to support `from tkinter import ...`
    tk.ttk = ttk
    tk.filedialog = filedialog
    tk.messagebox = messagebox
    # Mark as a package to be safe
    tk.__path__ = []  # type: ignore[attr-defined]
    sys.modules['tkinter'] = tk
    sys.modules['ttk'] = ttk
    sys.modules['tkinter.ttk'] = ttk
    sys.modules['tkinter.filedialog'] = filedialog
    sys.modules['tkinter.messagebox'] = messagebox


def test_pyqt6_build_command_list_defaults(monkeypatch):
    _stub_pyqt6()
    # Avoid importing PyQt6 in CI to keep tests light.
    # Instead, test the command assembly logic by stubbing the minimal API.
    m = import_module('GUI_pyqt6_WINFF')

    class Stub:
        # only the attributes used inside build_command_list
        def __init__(self):
            self.input_edit = type('E', (), {'text': lambda self: '/tmp/in.mp4'})()
            self.format_combo = type('C', (), {'currentText': lambda self: 'wmv'})()
            self.video_bitrate = type('E', (), {'text': lambda self: '204800'})()
            self.audio_bitrate = type('E', (), {'text': lambda self: '65536'})()
            self.resolution_combo = type('C', (), {'currentText': lambda self: 'original'})()
            self.video_codec_combo = type('C', (), {'currentText': lambda self: 'wmv2'})()
            self.audio_codec_combo = type('C', (), {'currentText': lambda self: 'wmav2'})()
            self.frame_rate = type('E', (), {'text': lambda self: '20'})()
            self.audio_sample_rate = type('E', (), {'text': lambda self: '22050'})()
            self.audio_channels = type('C', (), {'currentText': lambda self: '1'})()
            self.ffmpeg_path = type('E', (), {'text': lambda self: 'ffmpeg'})()
            self.same_dir_chk = type('C', (), {'isChecked': lambda self: True})()
            self.output_edit = type('E', (), {'text': lambda self: ''})()
            self.no_audio_chk = type('C', (), {'isChecked': lambda self: False})()

    w = Stub()
    args = m.FFmpegGuiPyQt6.build_command_list(w)
    assert args[0] == 'ffmpeg'
    assert '-i' in args and '/tmp/in.mp4' in args
    assert '-s' not in args  # resolution original means no -s


def test_tkinter_build_command_list_defaults(monkeypatch):
    _stub_tkinter()
    m = import_module('GUI_tkinter_WINFF')

    class Stub:
        def __init__(self):
            self.input_var = type('V', (), {'get': lambda self: '/tmp/in.mp4', 'set': lambda self, x: None})()
            self.format_var = type('V', (), {'get': lambda self: 'wmv'})()
            self.vbitrate_var = type('V', (), {'get': lambda self: '204800'})()
            self.abitrate_var = type('V', (), {'get': lambda self: '65536'})()
            self.resolution_var = type('V', (), {'get': lambda self: 'original'})()
            self.vcodec_var = type('V', (), {'get': lambda self: 'wmv2'})()
            self.acodec_var = type('V', (), {'get': lambda self: 'wmav2'})()
            self.fps_var = type('V', (), {'get': lambda self: '20'})()
            self.asamplerate_var = type('V', (), {'get': lambda self: '22050'})()
            self.achannels_var = type('V', (), {'get': lambda self: '1'})()
            self.ffmpeg_path_var = type('V', (), {'get': lambda self: 'ffmpeg'})()
            self.same_dir_var = type('V', (), {'get': lambda self: True})()
            self.output_dir_var = type('V', (), {'get': lambda self: ''})()
            self.no_audio_var = type('V', (), {'get': lambda self: False})()

        def _resolve_output_dir(self, inp: str) -> str:
            return '/tmp'

    app = Stub()
    args = m.FFmpegGuiTk.build_command_list(app)
    assert args[0] == 'ffmpeg'
    assert '-i' in args and '/tmp/in.mp4' in args
    assert '-s' not in args
