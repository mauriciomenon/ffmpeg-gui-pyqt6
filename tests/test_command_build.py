import os
import shlex
import types

# We'll import the GUI modules and call their build_command_list through a minimal shim.


def test_pyqt6_build_command_list_defaults(monkeypatch):
    import GUI_pyqt6_WINFF as m

    w = m.FFmpegGuiPyQt6()
    # simulate basic defaults
    w.input_edit.setText('/tmp/in.mp4')
    w.same_dir_chk.setChecked(True)
    w.set_default_options()

    args = w.build_command_list()
    assert args[0] == 'ffmpeg'
    assert '-i' in args and '/tmp/in.mp4' in args
    # ensure no -s when resolution is original
    assert '-s' not in args


def test_tkinter_build_command_list_defaults(monkeypatch):
    import GUI_tkinter_WINFF as m

    app = m.FFmpegGuiTk()
    app.input_var.set('/tmp/in.mp4')
    app.same_dir_var.set(True)
    app.set_default_options()

    args = app.build_command_list()
    assert args[0] == 'ffmpeg'
    assert '-i' in args and '/tmp/in.mp4' in args
    assert '-s' not in args
