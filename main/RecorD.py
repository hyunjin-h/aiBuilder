import contextlib
import queue
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

import numpy as np
import sounddevice as sd
import soundfile as sf


def file_writing_thread(*, q, **soundfile_args):
    """Write data from queue to file until *None* is received."""
    # NB: If you want fine-grained control about the buffering of the file, you
    #     can use Python's open() function (with the "buffering" argument) and
    #     pass the resulting file object to sf.SoundFile().
    with sf.SoundFile(**soundfile_args) as f:
        while True:
            data = q.get()
            if data is None:
                break
            f.write(data)


class SettingsWindow(Dialog):
    """Dialog window for choosing sound device."""

    def body(self, master):
        ttk.Label(master, text='Select host API:').pack(anchor='w')
        hostapi_list = ttk.Combobox(master, state='readonly', width=50)
        hostapi_list.pack()
        hostapi_list['values'] = [hostapi['name']
                                  for hostapi in sd.query_hostapis()]

        ttk.Label(master, text='Select sound device:').pack(anchor='w')
        device_ids = []
        device_list = ttk.Combobox(master, state='readonly', width=50)
        device_list.pack()

        def update_device_list(*args):
            hostapi = sd.query_hostapis(hostapi_list.current())
            nonlocal device_ids
            device_ids = [
                idx
                for idx in hostapi['devices']
                if sd.query_devices(idx)['max_output_channels'] > 0]
            device_list['values'] = [
                sd.query_devices(idx)['name'] for idx in device_ids]
            default = hostapi['default_output_device']
            if default >= 0:
                device_list.current(device_ids.index(default))
                device_list.event_generate('<<ComboboxSelected>>')

        def select_device(*args):
            self.result = device_ids[device_list.current()]

        hostapi_list.bind('<<ComboboxSelected>>', update_device_list)
        device_list.bind('<<ComboboxSelected>>', select_device)

        with contextlib.suppress(sd.PortAudioError):
            hostapi_list.current(sd.default.hostapi)
            hostapi_list.event_generate('<<ComboboxSelected>>')


class RecGui(tk.Tk):

    stream = None

    def __init__(self):
        super().__init__()

        self.title('Recording GUI')

        padding = 10

        f = ttk.Frame()

        self.rec_button = ttk.Button(f)
        self.rec_button.pack(side='left', padx=padding, pady=padding)


        self.settings_button = ttk.Button(
            f, text='settings', command=self.on_settings)
        self.settings_button.pack(side='left', padx=padding, pady=padding)

        f.pack(expand=True, padx=padding, pady=padding)

        self.file_label = ttk.Label(text='<file name>')
        self.file_label.pack(anchor='w')

        self.input_overflows = 0
        self.status_label = ttk.Label()
        self.status_label.pack(anchor='w')

        self.meter = ttk.Progressbar()
        self.meter['orient'] = 'horizontal'
        self.meter['mode'] = 'determinate'
        self.meter['maximum'] = 1.0
        self.meter.pack(fill='x')

        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)
        self.create_stream()

        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.peak = 0
        self.metering_q = queue.Queue(maxsize=1)

        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.init_buttons()
        self.update_gui()

    def create_stream(self, device=None):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(
            device=device, channels=1, callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status.input_overflow:
            # NB: This increment operation is not atomic, but this doesn't
            #     matter since no other thread is writing to the attribute.
            self.input_overflows += 1
        # NB: self.recording is accessed from different threads.
        #     This is safe because here we are only accessing it once (with a
        #     single bytecode instruction).
        if self.recording:
            self.audio_q.put(indata.copy())
            self.previously_recording = True
        else:
            if self.previously_recording:
                self.audio_q.put(None)
                self.previously_recording = False

        self.peak = max(self.peak, np.max(np.abs(indata)))
        try:
            self.metering_q.put_nowait(self.peak)
        except queue.Full:
            pass
        else:
            self.peak = 0

    def on_rec(self):
        self.settings_button['state'] = 'disabled'
        self.recording = True
        global filename
        filename = tempfile.mktemp(
            prefix='hanium_', suffix='.wav', dir='soundFiles')



        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='x',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                q=self.audio_q,
            ),
        )
        self.thread.start()

        # NB: File creation might fail!  For brevity, we don't check for this.

        self.rec_button['text'] = '🟥'
        self.rec_button['command'] = self.on_stop
        self.rec_button['state'] = 'normal'
        self.file_label['text'] = filename

    def on_stop(self, *args):
        self.rec_button['state'] = 'disabled'
        self.recording = False
        self.close_window()
        self.wait_for_thread()

    def wait_for_thread(self):
        # NB: Waiting time could be calculated based on stream.latency
        self.after(10, self._wait_for_thread)

    def _wait_for_thread(self):
        if self.thread.is_alive():
            self.wait_for_thread()
            return
        self.thread.join()
        self.init_buttons()

    def on_settings(self, *args):
        w = SettingsWindow(self, 'Settings')
        self.create_stream(device=w.result)

    def init_buttons(self):

        self.rec_button['text'] = '🛑'
        self.rec_button['command'] = self.on_rec
        if self.stream:
            self.rec_button['state'] = 'normal'
        self.settings_button['state'] = 'normal'

    def update_gui(self):
        self.status_label['text'] = 'input overflows: {}'.format(
            self.input_overflows)
        try:
            peak = self.metering_q.get_nowait()
        except queue.Empty:
            pass
        else:
            self.meter['value'] = peak
        self.after(100, self.update_gui)

    def close_window(self):
    #    if self.recording:
    #        self.on_stop()

        self.destroy()


def main():
    app = RecGui()
    app.mainloop()





if __name__ == '__main__':
    main()
