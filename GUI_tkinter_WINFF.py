#!/usr/bin/env python3
# GUI_tkinter_WINFF.py
# FFmpeg GUI em Tkinter com recursos: download dinâmico, winget, -an, ASF, resolução 'original'

import os
import sys
import json
import queue
import threading
import platform
import webbrowser
import zipfile
from io import BytesIO
import subprocess
import configparser
import tarfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import importlib
try:
	requests = importlib.import_module('requests')
except Exception:
	requests = None


class FFmpegGuiTk(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('Conversor de Vídeo Avançado (Tkinter)')
		self.geometry('960x720')
		self._build_ui()
		self.set_default_options()

	# -------------------- UI --------------------
	def _build_ui(self):
		pad = {'padx': 6, 'pady': 6}

		top = ttk.Frame(self)
		top.pack(fill='x', **pad)
		ttk.Button(top, text='About', command=self.show_about).pack(side='left')
		ttk.Button(top, text='Informações do vídeo', command=self.show_video_info).pack(side='right')
		ttk.Button(top, text='Baixar FFmpeg', command=self.download_ffmpeg_and_maybe_install).pack(side='right', padx=4)
		ttk.Button(top, text='Instalar FFmpeg (winget)', command=self.install_ffmpeg_via_winget).pack(side='right')

		frm = ttk.Frame(self)
		frm.pack(fill='x', **pad)
		ttk.Label(frm, text='Selecione o Arquivo de Vídeo:').grid(row=0, column=0, sticky='w')
		self.input_var = tk.StringVar()
		ttk.Entry(frm, textvariable=self.input_var, width=80).grid(row=0, column=1, sticky='we', padx=4)
		ttk.Button(frm, text='Procurar', command=self.select_file).grid(row=0, column=2)
		frm.columnconfigure(1, weight=1)

		ttk.Label(frm, text='Selecione o Diretório de Saída:').grid(row=1, column=0, sticky='w')
		self.output_dir_var = tk.StringVar()
		self.output_entry = ttk.Entry(frm, textvariable=self.output_dir_var, width=80)
		self.output_entry.grid(row=1, column=1, sticky='we', padx=4)
		ttk.Button(frm, text='Procurar', command=self.select_output_directory).grid(row=1, column=2)

		opts1 = ttk.Frame(self)
		opts1.pack(fill='x', **pad)
		self.same_dir_var = tk.BooleanVar(value=False)
		ttk.Checkbutton(opts1, text='Utilizar o mesmo diretório do arquivo de entrada', variable=self.same_dir_var, command=self.toggle_output_dir).pack(side='left')
		self.overwrite_var = tk.BooleanVar(value=True)
		ttk.Checkbutton(opts1, text='Sobrescrever arquivos existentes', variable=self.overwrite_var).pack(side='left', padx=10)

		grid = ttk.Frame(self)
		grid.pack(fill='x', **pad)

		row = 0
		ttk.Label(grid, text='Formato de Saída:').grid(row=row, column=0, sticky='w')
		self.format_var = tk.StringVar(value='wmv')
		ttk.Combobox(grid, textvariable=self.format_var, values=['mp4','avi','mkv','flv','mov','mp3','wmv','asf'], width=12, state='readonly').grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Codec de Vídeo:').grid(row=row, column=0, sticky='w')
		self.vcodec_var = tk.StringVar(value='wmv2')
		ttk.Combobox(grid, textvariable=self.vcodec_var, values=['auto','libx264','libx265','mpeg4','wmv2'], width=12, state='readonly').grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Codec de Áudio:').grid(row=row, column=0, sticky='w')
		self.acodec_var = tk.StringVar(value='wmav2')
		self.acodec_combo = ttk.Combobox(grid, textvariable=self.acodec_var, values=['auto','aac','mp3','ac3','wmav2'], width=12, state='readonly')
		self.acodec_combo.grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Resolução:').grid(row=row, column=0, sticky='w')
		self.resolution_var = tk.StringVar(value='original')
		ttk.Combobox(grid, textvariable=self.resolution_var, values=['original','1920x1080','1280x720','640x480','320x240'], width=12, state='readonly').grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Bitrate de Vídeo:').grid(row=row, column=0, sticky='w')
		self.vbitrate_var = tk.StringVar(value='204800')
		ttk.Entry(grid, textvariable=self.vbitrate_var, width=12).grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Bitrate de Áudio:').grid(row=row, column=0, sticky='w')
		self.abitrate_var = tk.StringVar(value='65536')
		self.abitrate_entry = ttk.Entry(grid, textvariable=self.abitrate_var, width=12)
		self.abitrate_entry.grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='FPS (frame rate):').grid(row=row, column=0, sticky='w')
		self.fps_var = tk.StringVar(value='20')
		ttk.Entry(grid, textvariable=self.fps_var, width=12).grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Audio sample rate:').grid(row=row, column=0, sticky='w')
		self.asamplerate_var = tk.StringVar(value='22050')
		self.asamplerate_entry = ttk.Entry(grid, textvariable=self.asamplerate_var, width=12)
		self.asamplerate_entry.grid(row=row, column=1, sticky='w')

		row += 1
		ttk.Label(grid, text='Audio channels:').grid(row=row, column=0, sticky='w')
		self.achannels_var = tk.StringVar(value='1')
		self.achannels_combo = ttk.Combobox(grid, textvariable=self.achannels_var, values=['1','2'], width=12, state='readonly')
		self.achannels_combo.grid(row=row, column=1, sticky='w')

		row += 1
		self.no_audio_var = tk.BooleanVar(value=False)
		ttk.Checkbutton(grid, text='Arquivo sem áudio (-an)', variable=self.no_audio_var, command=self.on_no_audio_change).grid(row=row, column=0, columnspan=2, sticky='w')

		# ffmpeg path
		pathf = ttk.Frame(self)
		pathf.pack(fill='x', **pad)
		ttk.Label(pathf, text='Caminho do Executável FFmpeg:').pack(side='left')
		self.ffmpeg_path_var = tk.StringVar(value='ffmpeg')
		self.ffmpeg_path_entry = ttk.Entry(pathf, textvariable=self.ffmpeg_path_var, width=60)
		self.ffmpeg_path_entry.pack(side='left', fill='x', expand=True, padx=4)
		ttk.Button(pathf, text='Procurar', command=self.select_ffmpeg).pack(side='left')

		# command display
		ttk.Label(self, text='Comando FFmpeg:').pack(anchor='w', **pad)
		self.cmd_text = tk.Text(self, height=5)
		self.cmd_text.pack(fill='x', padx=6)

		# bottom buttons
		btns = ttk.Frame(self)
		btns.pack(fill='x', pady=8)
		ttk.Button(btns, text='Opções Padrão', command=self.set_default_options).pack(side='left')
		ttk.Button(btns, text='Carregar Configuração', command=self.load_config).pack(side='left', padx=6)
		ttk.Button(btns, text='Salvar Configuração', command=self.save_config).pack(side='left')
		self.convert_btn = ttk.Button(btns, text='Converter', command=self.convert_video)
		self.convert_btn.pack(side='right')
		self.cancel_btn = ttk.Button(btns, text='Cancelar', command=self.cancel_convert, state='disabled')
		self.cancel_btn.pack(side='right', padx=6)

		# runtime process state
		self._proc = None
		self._log_q = queue.Queue()
		self._reader_thread = None

	# -------------------- Actions --------------------
	def select_file(self):
		file = filedialog.askopenfilename(title='Selecione o arquivo de vídeo')
		if file:
			self.input_var.set(file)
			self.update_command_display()

	def select_output_directory(self):
		d = filedialog.askdirectory(title='Selecione o diretório de saída')
		if d:
			self.output_dir_var.set(d)
			self.update_command_display()

	def toggle_output_dir(self):
		self.output_entry.configure(state='disabled' if self.same_dir_var.get() else 'normal')
		self.update_command_display()

	def select_ffmpeg(self):
		file = filedialog.askopenfilename(title='Selecione o FFmpeg')
		if file:
			self.ffmpeg_path_var.set(file)
			self.update_command_display()

	def set_default_options(self):
		# Defaults already seeded in variables; ensure resolution default and update display
		self.resolution_var.set('original')
		self.no_audio_var.set(False)
		self.on_no_audio_change()
		self.update_command_display()

	def load_config(self):
		file = filedialog.askopenfilename(title='Carregar Configuração', filetypes=[('INI Files','*.ini')])
		if not file:
			return
		cp = configparser.ConfigParser(); cp.read(file)
		d = cp['DEFAULT'] if 'DEFAULT' in cp else {}
		self.ffmpeg_path_var.set(d.get('ffmpeg_path','ffmpeg'))
		self.format_var.set(d.get('default_format','wmv'))
		self.output_dir_var.set(d.get('default_output_dir',''))
		self.vcodec_var.set(d.get('default_video_codec','wmv2'))
		self.acodec_var.set(d.get('default_audio_codec','wmav2'))
		self.resolution_var.set(d.get('default_resolution','original'))
		self.vbitrate_var.set(d.get('video_bitrate','204800'))
		self.abitrate_var.set(d.get('audio_bitrate','65536'))
		self.fps_var.set(d.get('frame_rate','20'))
		self.asamplerate_var.set(d.get('audio_sample_rate','22050'))
		self.achannels_var.set(d.get('audio_channels','1'))
		self.same_dir_var.set(d.get('use_same_directory','False')=='True')
		self.overwrite_var.set(d.get('overwrite_existing','True')=='True')
		self.no_audio_var.set(d.get('no_audio','False')=='True')
		self.on_no_audio_change()
		self.update_command_display()

	def save_config(self):
		file = filedialog.asksaveasfilename(title='Salvar Configuração', defaultextension='.ini', filetypes=[('INI Files','*.ini')])
		if not file:
			return
		cp = configparser.ConfigParser()
		cp['DEFAULT'] = {
			'ffmpeg_path': self.ffmpeg_path_var.get(),
			'default_format': self.format_var.get(),
			'default_output_dir': self.output_dir_var.get(),
			'default_video_codec': self.vcodec_var.get(),
			'default_audio_codec': self.acodec_var.get(),
			'default_resolution': self.resolution_var.get(),
			'video_bitrate': self.vbitrate_var.get(),
			'audio_bitrate': self.abitrate_var.get(),
			'frame_rate': self.fps_var.get(),
			'audio_sample_rate': self.asamplerate_var.get(),
			'audio_channels': self.achannels_var.get(),
			'use_same_directory': str(self.same_dir_var.get()),
			'overwrite_existing': str(self.overwrite_var.get()),
			'no_audio': str(self.no_audio_var.get()),
		}
		with open(file, 'w') as f:
			cp.write(f)

	# -------------------- Command build --------------------
	def _resolve_output_dir(self, inp: str) -> str:
		if self.same_dir_var.get() and inp:
			return os.path.dirname(inp)
		return self.output_dir_var.get().strip()

	def build_command_list(self):
		inp = self.input_var.get().strip()
		if not inp:
			return []

		fmt = self.format_var.get()
		vbitrate = self.vbitrate_var.get().strip()
		abitrate = self.abitrate_var.get().strip()
		resolution = self.resolution_var.get()
		vcodec = self.vcodec_var.get()
		acodec = self.acodec_var.get()
		fps = self.fps_var.get().strip()
		asamplerate = self.asamplerate_var.get().strip()
		achannels = self.achannels_var.get().strip()
		ffmpeg = self.ffmpeg_path_var.get().strip() or 'ffmpeg'

		out_dir = self._resolve_output_dir(inp)
		out_file = os.path.join(out_dir, os.path.splitext(os.path.basename(inp))[0] + '.' + fmt) if inp else ''

		args = [ffmpeg, '-y', '-i', inp]
		if vbitrate:
			args += ['-b:v', vbitrate]
		if self.no_audio_var.get():
			args += ['-an']
		elif abitrate:
			args += ['-b:a', abitrate]
		if resolution != 'original':
			args += ['-s', resolution]
		if fps:
			args += ['-r', fps]
		if not self.no_audio_var.get() and asamplerate:
			args += ['-ar', asamplerate]
		if not self.no_audio_var.get() and achannels:
			args += ['-ac', achannels]
		if vcodec != 'auto':
			args += ['-vcodec', vcodec]
		if not self.no_audio_var.get() and acodec != 'auto':
			args += ['-acodec', acodec]
		if out_file:
			args += [out_file]
		return args

	def update_command_display(self):
		import shlex
		args = self.build_command_list()
		self.cmd_text.delete('1.0', 'end')
		if not args:
			return
		self.cmd_text.insert('1.0', ' '.join(shlex.quote(a) for a in args))

	def _append_log(self, text: str):
		# Efficiently append to the end without rewriting everything
		if self.cmd_text.get('1.0', 'end-1c'):
			self.cmd_text.insert('end', '\n' + text)
		else:
			self.cmd_text.insert('end', text)
		self.cmd_text.see('end')

	def _reader_worker(self):
		try:
			assert self._proc is not None
			for line in self._proc.stdout:
				self._log_q.put(line.rstrip())
		except Exception as e:
			self._log_q.put(f"[erro leitor]: {e}")

	def _poll_logs(self):
		try:
			while True:
				line = self._log_q.get_nowait()
				self._append_log(line)
		except queue.Empty:
			pass
		# if process still alive, reschedule; else finalize
		if self._proc is not None and self._proc.poll() is None:
			self.after(200, self._poll_logs)
		else:
			code = None if self._proc is None else self._proc.returncode
			self._proc = None
			self.convert_btn.configure(state='normal')
			self.cancel_btn.configure(state='disabled')
			if code == 0:
				messagebox.showinfo('Sucesso', 'Vídeo convertido com sucesso!')
			elif code is not None:
				messagebox.showerror('Erro', f'Falha ao converter vídeo (código {code}).')

	def cancel_convert(self):
		if self._proc is not None and self._proc.poll() is None:
			self._append_log('Cancelando conversão...')
			try:
				self._proc.terminate()
			except Exception:
				pass

	def convert_video(self):
		if self._proc is not None and self._proc.poll() is None:
			messagebox.showwarning('Em execução', 'Uma conversão já está em andamento.')
			return
		args = self.build_command_list()
		if not args:
			messagebox.showwarning('Erro', 'Preencha os campos necessários')
			return
		self._append_log('Iniciando conversão...')
		try:
			self._proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
			self._reader_thread = threading.Thread(target=self._reader_worker, daemon=True)
			self._reader_thread.start()
			self.convert_btn.configure(state='disabled')
			self.cancel_btn.configure(state='normal')
			self.after(200, self._poll_logs)
		except Exception as e:
			self._proc = None
			messagebox.showerror('Erro', f'Falha ao iniciar ffmpeg: {e}')

	# -------------------- Info/About --------------------
	def show_about(self):
		messagebox.showinfo('About', 'Mauricio Menon (+AI)\nhttps://github.com/mauriciomenon\nTkinter version of the GUI')

	def _resolve_ffprobe(self) -> str:
		configured = self.ffmpeg_path_var.get().strip()
		ffprobe_name = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
		if configured and os.path.isabs(configured):
			base = configured if os.path.isdir(configured) else os.path.dirname(configured)
			cand = os.path.join(base, ffprobe_name)
			if os.path.exists(cand):
				return cand
		return ffprobe_name  # via PATH

	def show_video_info(self):
		inp = self.input_var.get().strip()
		if not inp:
			messagebox.showwarning('Atenção', 'Nenhum arquivo selecionado')
			return
		ffprobe = self._resolve_ffprobe()
		try:
			p = subprocess.run([ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', inp],
							   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
			data = json.loads(p.stdout or '{}')
			info_text = json.dumps(data, indent=2, ensure_ascii=False)
			self._show_text_dialog('Informações detalhadas do vídeo', info_text)
		except Exception as e:
			messagebox.showerror('Erro', f'Falha ao obter info: {e}')

	def _show_text_dialog(self, title, text):
		win = tk.Toplevel(self)
		win.title(title)
		txt = tk.Text(win, width=100, height=30)
		txt.pack(fill='both', expand=True)
		txt.insert('1.0', text)
		txt.configure(state='disabled')
		ttk.Button(win, text='Fechar', command=win.destroy).pack(pady=6)

	# -------------------- Download/Install FFmpeg --------------------
	def _get_latest_ffmpeg_windows_zip_url(self) -> str:
		# GitHub API (BtbN/FFmpeg-Builds) + fallback
		try:
			import urllib.request, json as _json
			req = urllib.request.Request('https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest', headers={'User-Agent': 'ffmpeg-gui'})
			with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
				if resp.status == 200:
					data = _json.loads(resp.read().decode('utf-8'))
					for asset in data.get('assets', []):
						name = asset.get('name','')
						if name.endswith('win64-gpl.zip'):
							return asset.get('browser_download_url')
		except Exception:
			pass
		return 'https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip'

	def _extract_ffmpeg_zip(self, zip_bytes: bytes) -> str | None:
		base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin'))
		os.makedirs(base_dir, exist_ok=True)
		with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
			self._safe_zip_extract(zf, base_dir)
		for root, _dirs, files in os.walk(base_dir):
			for f in files:
				if f.lower() == ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'):
					return os.path.join(root, f)
		return None

	def _http_get(self, url: str, timeout: int = 60) -> bytes:
		"""Download com requests (se disponível) e fallback para urllib."""
		if requests is not None:
			try:
				r = requests.get(url, timeout=timeout)
				r.raise_for_status()
				return r.content
			except Exception:
				pass
		import urllib.request
		with urllib.request.urlopen(url, timeout=timeout) as resp:  # nosec B310
			return resp.read()

	def download_ffmpeg_and_maybe_install(self):
		q = queue.Queue()

		def worker():
			try:
				sysname = platform.system()
				if sysname == 'Windows':
					url = self._get_latest_ffmpeg_windows_zip_url()
					content = self._http_get(url, timeout=60)
					ff = self._extract_ffmpeg_zip(content)
					if ff:
						q.put(('ok', ff, 'FFmpeg baixado e extraído com sucesso.'))
					else:
						q.put(('err', None, 'Não foi possível localizar o executável ffmpeg após extração.'))
				elif sysname == 'Linux':
					arch = platform.machine().lower()
					url = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz' if arch in ('aarch64','arm64') else 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
					content = self._http_get(url, timeout=60)
					base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin'))
					os.makedirs(base_dir, exist_ok=True)
					with tarfile.open(fileobj=BytesIO(content), mode='r:xz') as tf:
						self._safe_tar_extract(tf, base_dir)
					ffpath = None
					for root, _d, files in os.walk(base_dir):
						for f in files:
							if f == 'ffmpeg':
								ffpath = os.path.join(root, f)
								break
						if ffpath:
							break
					if ffpath:
						q.put(('ok', ffpath, 'FFmpeg baixado e pronto (build estático).'))
					else:
						q.put(('err', None, 'Não foi possível localizar o ffmpeg extraído.'))
				else:
					webbrowser.open('https://formulae.brew.sh/formula/ffmpeg')
					q.put(('info', None, 'No macOS, instale via Homebrew: brew install ffmpeg'))
			except Exception as e:
				q.put(('err', None, f'Falha no download: {e}'))

		def poll():
			try:
				typ, path, msg = q.get_nowait()
			except queue.Empty:
				self.after(200, poll)
				return
			if typ == 'ok':
				if path:
					self.ffmpeg_path_var.set(path)
				messagebox.showinfo('Info', msg)
			elif typ == 'info':
				messagebox.showinfo('Info', msg)
			else:
				messagebox.showerror('Erro', msg)

		threading.Thread(target=worker, daemon=True).start()
		self.after(200, poll)

	def _safe_tar_extract(self, tf: tarfile.TarFile, base_dir: str):
		base = os.path.realpath(base_dir)
		for member in tf.getmembers():
			member_path = os.path.realpath(os.path.join(base, member.name))
			if not member_path.startswith(base + os.sep) and member_path != base:
				raise RuntimeError(f"Entrada insegura no tar: {member.name}")
		tf.extractall(base)

	def _safe_zip_extract(self, zf: zipfile.ZipFile, base_dir: str):
		base = os.path.realpath(base_dir)
		for zi in zf.infolist():
			name = zi.filename
			# reject absolute paths or drive letters on Windows
			if os.path.isabs(name) or (len(name) > 1 and name[1] == ':'):
				raise RuntimeError(f"Entrada insegura no zip (absoluta): {name}")
			dest = os.path.realpath(os.path.join(base, name))
			if not dest.startswith(base + os.sep) and dest != base:
				raise RuntimeError(f"Entrada insegura no zip: {name}")
		# after validation, extract members
		for zi in zf.infolist():
			dest = os.path.realpath(os.path.join(base, zi.filename))
			if zi.is_dir() or zi.filename.endswith('/'):
				os.makedirs(dest, exist_ok=True)
				continue
			os.makedirs(os.path.dirname(dest), exist_ok=True)
			with zf.open(zi, 'r') as src, open(dest, 'wb') as out:
				out.write(src.read())

	def install_ffmpeg_via_winget(self):
		if platform.system() != 'Windows':
			messagebox.showerror('Erro', 'Instalação via winget só está disponível no Windows.')
			return

		q = queue.Queue()

		def worker():
			try:
				cmds = [
					['winget', 'install', '-e', '--id', 'Gyan.FFmpeg'],
					['winget', 'install', '-e', '--id', 'FFmpeg.FFmpeg']
				]
				ok = False
				for c in cmds:
					p = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					if p.returncode == 0:
						ok = True
						break
				q.put(('ok' if ok else 'err', None))
			except Exception as e:
				q.put(('err', str(e)))

		def poll():
			try:
				typ, _ = q.get_nowait()
			except queue.Empty:
				self.after(200, poll)
				return
			if typ == 'ok':
				self.ffmpeg_path_var.set('ffmpeg')
				messagebox.showinfo('Info', 'FFmpeg instalado via winget.')
			else:
				messagebox.showerror('Erro', 'Falha ao instalar via winget.')

		threading.Thread(target=worker, daemon=True).start()
		self.after(200, poll)

	# -------------------- Audio toggle --------------------
	def on_no_audio_change(self):
		disabled = self.no_audio_var.get()
		state = 'disabled' if disabled else 'normal'
		self.acodec_combo.configure(state='readonly' if not disabled else 'disabled')
		self.abitrate_entry.configure(state=state)
		self.asamplerate_entry.configure(state=state)
		self.achannels_combo.configure(state='readonly' if not disabled else 'disabled')
		self.update_command_display()


if __name__ == '__main__':
	app = FFmpegGuiTk()
	app.mainloop()