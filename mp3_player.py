import tkinter as tk
from tkinter import filedialog, ttk
from pygame import mixer
import time
import threading

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("IVMUSIC V0.1")
        self.root.geometry("400x300")

        mixer.init()

        self.playlist = []
        self.current_song = ""
        self.paused = False

        self.song_label = tk.Label(root, text="No song loaded", bg="white", relief="sunken", anchor="w")
        self.song_label.pack(fill="x", padx=10, pady=5)

        self.play_button = tk.Button(root, text="▶", command=self.play_pause_song)
        self.play_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="⏹", command=self.stop_song)
        self.stop_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load", command=self.load_song)
        self.load_button.pack(pady=5)

        self.slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=self.set_position)
        self.slider.pack(fill="x", padx=10, pady=5)

        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.daemon = True
        self.update_thread.start()

    def load_song(self):
        song = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song:
            self.playlist.append(song)
            self.current_song = song
            self.song_label.config(text=song.split("/")[-1])
            self.slider.config(to=self.get_song_length(song))

    def play_pause_song(self):
        if self.paused:
            mixer.music.unpause()
            self.play_button.config(text="⏸")
            self.paused = False
        else:
            if not mixer.music.get_busy():
                mixer.music.load(self.current_song)
                mixer.music.play()
            else:
                mixer.music.pause()
            self.play_button.config(text="▶" if self.paused else "⏸")
            self.paused = not self.paused

    def stop_song(self):
        mixer.music.stop()
        self.play_button.config(text="▶")
        self.paused = False

    def set_position(self, val):
        pos = float(val)
        mixer.music.set_pos(pos)

    def update(self):
        while True:
            if mixer.music.get_busy() and not self.paused:
                pos = mixer.music.get_pos() / 1000
                self.slider.set(pos)
                if pos >= self.slider.cget("to"):
                    self.stop_song()
            time.sleep(1)

    def get_song_length(self, song):
        mixer.music.load(song)
        return mixer.Sound(song).get_length()

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Player(root)
    root.mainloop()
