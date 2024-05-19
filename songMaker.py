import tkinter as tk
from tkinter import ttk
import pygame
import time
from threading import Thread


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SongMaker(tk.Tk, metaclass=Singleton):
    ROWS = 8
    COLS = 30
    row_colors = ["#FF0000", "#FFA500", "#FFFF00", "#008000",
                  "#0000FF", "#FFC0CB", "#FF00FF", "#000000"]

    def __init__(self):
        super().__init__()

        self.title("SongMaker")
        self.geometry("600x400")

        self.buttons = [[None for _ in range(self.COLS)]
                        for _ in range(self.ROWS)]
        self.original_colors = [
            [None for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.create_widgets()
        pygame.mixer.init()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="멜로디 작성",
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        # 버튼 그리드
        grid_frame = tk.Frame(self)
        grid_frame.pack()

        for row in range(self.ROWS):
            for col in range(self.COLS):
                btn = tk.Button(grid_frame, bg="white", width=2, height=1,
                                command=lambda r=row, c=col: self.on_button_click(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

        # 재생 및 리셋 버튼
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        play_button = tk.Button(
            control_frame, text="재생", command=self.on_play_click)
        play_button.pack(side="left", padx=5)

        reset_button = tk.Button(
            control_frame, text="리셋", command=self.on_reset_click)
        reset_button.pack(side="left", padx=5)

        # 간격 슬라이더
        self.interval_var = tk.IntVar(value=3)
        interval_slider = ttk.Scale(
            control_frame, from_=0, to=10, orient="horizontal", variable=self.interval_var)
        interval_slider.pack(side="left", padx=5)
        interval_slider.bind("<ButtonRelease-1>", self.on_slider_release)

    def on_button_click(self, row, col):
        btn = self.buttons[row][col]
        current_color = btn.cget("bg")
        wav_file_path = self.melody_find(row)

        if current_color == "white":
            btn.config(bg=self.row_colors[row])
            self.play_wav(wav_file_path)
        else:
            btn.config(bg="white")

        print(f"셀 클릭: ({row}, {col})")

    def melody_find(self, row):
        file_paths = [
            "./Sounds/do.wav",
            "./Sounds/re.wav",
            "./Sounds/mi.wav",
            "./Sounds/fa.wav",
            "./Sounds/sol.wav",
            "./Sounds/la.wav",
            "./Sounds/si.wav",
            "./Sounds/do2.wav"
        ]
        return file_paths[row]

    def play_wav(self, wav_file_path):
        try:
            pygame.mixer.music.load(wav_file_path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"{wav_file_path} 재생 오류: {e}")

    def on_play_click(self):
        print("재생 버튼 클릭")
        Thread(target=self.play_sequence).start()

    def play_sequence(self):
        for col in range(self.COLS):
            for row in range(self.ROWS):
                btn = self.buttons[row][col]
                if btn.cget("bg") == self.row_colors[row]:
                    wav_file_path = self.melody_find(row)
                    self.play_wav(wav_file_path)
            self.update_button_colors(col)
            time.sleep((10 - self.interval_var.get()) / 10)

    def update_button_colors(self, col):
        for row in range(self.ROWS):
            btn = self.buttons[row][col]
            current_color = btn.cget("bg")
            transparent_sky_blue = "#87CEEB"
            combined_color = self.mix_colors(
                current_color, transparent_sky_blue)

            self.original_colors[row][col] = current_color
            btn.config(bg=combined_color)

        if col > 0:
            self.restore_previous_colors(col - 1)

    def mix_colors(self, color1, color2):
        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)
        r = (r1 + r2) // 2 // 256
        g = (g1 + g2) // 2 // 256
        b = (b1 + b2) // 2 // 256
        return f"#{r:02x}{g:02x}{b:02x}"

    def restore_previous_colors(self, col):
        for row in range(self.ROWS):
            btn = self.buttons[row][col]
            btn.config(bg=self.original_colors[row][col])

    def on_reset_click(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.buttons[row][col].config(bg="white")
        print("리셋 버튼 클릭")

    def on_slider_release(self, event):
        print("슬라이더 값:", self.interval_var.get())


if __name__ == "__main__":
    app = SongMaker()
    app.mainloop()
