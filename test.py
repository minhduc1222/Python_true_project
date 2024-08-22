import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Real-Time Video Player")
        
        # Load video
        self.video = cv2.VideoCapture(video_path)
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Setup canvas to display video frames
        self.canvas = Label(root)
        self.canvas.pack()

        # Play button
        self.play_button = Button(root, text="Play Video", command=self.play_video)
        self.play_button.pack()

        # Stop button
        self.stop_button = Button(root, text="Stop Video", command=self.stop_video)
        self.stop_button.pack()

        self.playing = False

    def play_video(self):
        self.playing = True
        self.update_video()

    def update_video(self):
        if self.playing:
            ret, frame = self.video.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.imgtk = imgtk
                self.canvas.configure(image=imgtk)
                self.root.after(10, self.update_video)  # Update every 10ms
            else:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video

    def stop_video(self):
        self.playing = False

    def on_closing(self):
        self.playing = False
        self.video.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root, "path_to_your_video.mp4")
    root.protocol("WM_DELETE_WINDOW", player.on_closing)
    root.mainloop()
