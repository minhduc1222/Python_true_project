import tkinter as tk
import font_manager as fonts
import subprocess

def check_video_clicked():
    subprocess.run(['python', 'Check_video.py'])
    status_lbl.configure(text="Check Videos button was clicked!")

def create_video_list_clicked():
    subprocess.run(['python', 'Create_video_list.py'])
    status_lbl.configure(text="Create Video List button was clicked!")

def update_video_clicked():
    subprocess.run(['python', 'Update_rating.py'])
    status_lbl.configure(text="Update Videos button was clicked!")
    
window = tk.Tk()
window.geometry("520x150")
window.title("Video Player")

fonts.configure()

header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below")
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

check_videos_btn = tk.Button(window, text="Check Videos", command=check_video_clicked)
check_videos_btn.grid(row=1, column=0, padx=10, pady=10)

create_video_list_btn = tk.Button(window, text="Create Video List", command=create_video_list_clicked)
create_video_list_btn.grid(row=1, column=1, padx=10, pady=10)

update_videos_btn = tk.Button(window, text="Update Videos", command=update_video_clicked)
update_videos_btn.grid(row=1, column=2, padx=10, pady=10)

status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()
