import tkinter as tk
from tkinter import messagebox
import font_manager as font

from read_write_csv import read_csv, write_to_csv

LIBRARY_CSV_FILE = 'library_video_list.csv'

def add_video():
    name = name_entry.get()
    director = author_entry.get()
    video_length = video_length_entry.get()
    rating = rating_entry.get()
    
    if not (name and director and video_length and rating):
        messagebox.showerror("Input Error", "All fields must be filled out!")
        return

    try:
        video_length = int(video_length)
        rating = float(rating)
        if video_length < 0 or rating < 0 or rating > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Video length must be an integer and rating must be a number between 0 and 10!")
        return

    data = read_csv(LIBRARY_CSV_FILE)

    if name.strip().lower().replace(" ", "") in [item['name'].strip().lower().replace(" ", "") for item in data.values()]:
        messagebox.showerror("Input Error", "Video already exists in the library!")
        return
    
    if data:
        max_id = max(int(key) for key in data.keys())
        next_key = str(max_id + 1)
    else:
        next_key = "1"

    data[next_key] = {'name': name, 'director': director, 'video_length': video_length, 'rating': rating, 'play_count': 0}
    
    write_to_csv(data, LIBRARY_CSV_FILE)
    messagebox.showinfo("Success", f"Added new video with key {next_key}.")

# Create the main window
root = tk.Tk()
root.title("Add Video Information")

# Create and pack the input fields with labels aligned to the left
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Author:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
author_entry = tk.Entry(root, width=30)
author_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Video Length:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
video_length_entry = tk.Entry(root, width=30)
video_length_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Rating:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
rating_entry = tk.Entry(root, width=30)
rating_entry.grid(row=3, column=1, padx=10, pady=5)

# Create and pack the Add button
add_button = tk.Button(root, text="Add Video", command=add_video)
add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
if __name__ == '__main__':
    font.configure()
    root.mainloop()
