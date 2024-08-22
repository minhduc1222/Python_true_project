import tkinter as tk
from tkinter import ttk, messagebox

import tkinter.scrolledtext as tkst
import font_manager as fonts
import subprocess

from read_write_csv import read_csv, write_to_csv

MY_CSV_FILE = 'my_video_playlist.csv'
LIBRARY_CSV_FILE = 'library_video_list.csv'

class Create_video_lists():
    def __init__(self, window):
        self.window = window
        window.geometry("1000x400")
        window.title("Create_video_list")

        self.current_video_id = None
        self.playing = False
        self.target_video_length = 0
        self.video_length = tk.IntVar(value=0)
        self.time_count = tk.IntVar(value=0)
        self.play_count_increased = False
        self.create_widgets()
        self.populate_scrolled_text()

    def create_widgets(self):
        # Filter widgets
        self.filter_label = tk.Label(self.window, text="Enter: ")
        self.filter_label.grid(row=0, column=0, pady=10, sticky="E")

        self.filter_combobox = ttk.Combobox(self.window, width=5, values=["ID", "Name"])
        self.filter_combobox.grid(row=0, column=1, pady=10, sticky="W")
        self.filter_combobox.current(0)

        self.video_input_entry = tk.Entry(self.window, width=25)
        self.video_input_entry.grid(row=0, column=2, padx=10, pady=10)
        self.video_input_entry.bind("<KeyRelease>", self.apply_filter) 

        check_video_btn = tk.Button(self.window, text="Check", command=self.check_video)
        check_video_btn.grid(row=0, column=3, padx=10, pady=10, sticky="W")

        clear_all_btn = tk.Button(self.window, text="Clear All", command=self.clear_all)
        clear_all_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # ScrolledText widget
        self.list_txt = tkst.ScrolledText(self.window, width=45, height=12, cursor="arrow", state=tk.DISABLED)
        self.list_txt.grid(row=2, column=0, columnspan=4, rowspan=4, sticky="W", padx=10, pady=10)
        self.list_txt.bind("<Button-1>", self.on_item_click)

        self.video_txt = tk.Text(self.window, width=24, height=4, wrap="none", state=tk.DISABLED)
        self.video_txt.grid(row=2, column=4, columnspan=3, sticky="NW", padx=10, pady=10)

        self.play_count_txt = tk.Text(self.window, width=24, height=1, wrap="none", state=tk.DISABLED)
        self.play_count_txt.grid(row=3, column=4, columnspan=3, sticky="NW", padx=10, pady=10)

        # Play and reset buttons with video length label
        self.play_button = tk.Button(self.window, text="Play", command=self.play_video)
        self.play_button.grid(row=4, column=4, padx=10, pady=10)

        self.time_count_display = tk.Label(self.window, textvariable=self.time_count)
        self.time_count_display.grid(row=4, column=5, pady=10, sticky="W")

        # self.division_label = tk.Label(self.window, text="/")
        # self.division_label.grid(row=4, column=5, padx=10, pady=10)

        self.video_length_display = tk.Label(self.window, textvariable=self.video_length)
        self.video_length_display.grid(row=4, column=5, padx=10, pady=10, sticky="E")

        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", length=150, mode="determinate")
        self.progress_bar.grid(row=4, column=6, columnspan=2, padx=10, pady=10, sticky="E")

        # Configure ScrolledText to hide the cursor
        self.list_txt.config(insertbackground=self.list_txt.cget("background"))

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_video_length)
        self.reset_button.grid(row=4, column=8, padx=10, pady=10)

        # Add video to playlist button
        create_video_btn = tk.Button(self.window, text="Add to playlist", command=self.add_to_playlist)
        create_video_btn.grid(row=0, column=4, columnspan=2, padx=10, pady=10, sticky='E')

        # Update video button
        update_video_btn = tk.Button(self.window, text="Update Rating", command=self.update_video)
        update_video_btn.grid(row=0, column=6, columnspan=2, padx=10, pady=10, sticky="W")

        # Delete video button
        delete_video_btn = tk.Button(self.window, text="Delete", width=5, command=self.delete_video)
        delete_video_btn.grid(row=2, column=7, padx=10, pady=10, sticky="NE")
        
        # Back button
        back_btn = tk.Button(self.window, text="<-- Back", command=self.window.destroy)
        back_btn.grid(row=0, column=8, padx=10, pady=10, sticky="W")
        
    def populate_scrolled_text(self):

        my_info = read_csv(MY_CSV_FILE)
        self.list_txt.config(state=tk.NORMAL)
        self.video_input_entry.delete(0, tk.END)
        self.list_txt.delete(1.0, tk.END)
        for key, info in my_info.items():
            self.list_txt.insert(tk.END, f"{key}. {info['name']}\n")
        self.list_txt.config(state=tk.DISABLED)

    def apply_filter(self, event):
        filter_by = self.filter_combobox.get()
        filter_value = self.video_input_entry.get()

        if filter_by == "ID":
            try:
                filter_value = str(filter_value)
            except ValueError:
                filter_value = None
        elif filter_by == "Name":
            try:
                filter_value = str(filter_value)
            except ValueError:
                filter_value = None
    
    def check_video(self, mode="input"):
        filter_by = self.filter_combobox.get()

        video_info = read_csv(LIBRARY_CSV_FILE)

        if mode == "input":
            input_value = self.video_input_entry.get().strip()
            self.list_txt.tag_remove("highlight", "1.0", tk.END)
            if input_value == "" and self.current_video_id is None:
                messagebox.showerror("Input Error", "Video Input fields must be filled out!")
                return

            if filter_by == "ID":
                ids = [key for key, info in video_info.items() if key.lstrip('0') == input_value.lstrip('0')]
            elif filter_by == "Name":
                ids = [key for key, info in video_info.items() if info['name'].strip().lower() == input_value.strip().lower()]

        elif mode == "click":
            input_value = self.current_video_id
            if input_value == "" and self.current_video_id is None:
                messagebox.showerror("Input Error", "Video Input fields must be filled out!")
                return

            ids = [key for key, info in video_info.items() if key == input_value]

        if not ids:
            messagebox.showerror(f"Invalid Input", f"Video with {filter_by} '{input_value}' not found.")
            return

        video_id = ids[0]
        if video_id is not None:
            video_details = video_info[video_id]
            details = (f"Name: {video_details['name']}\n"
                    f"Video Length: {video_details['video_length']}\n"
                    f"Rating: {video_details['rating']}\n"
                    f"Director: {video_details['director']}\n")
            self.video_txt.config(state=tk.NORMAL)
            self.video_txt.delete(1.0, tk.END)
            self.play_count_txt.config(state=tk.NORMAL)
            self.play_count_txt.delete(1.0, tk.END)
            self.video_txt.insert(tk.END, details)
            self.video_txt.config(state=tk.DISABLED)

        self.check_play_count(video_id)


    def check_play_count(self, id):

        my_info = read_csv(MY_CSV_FILE)
        if id in my_info:
            play_count = f"Play Count: {my_info[id].get('play_count', 0)}"
            self.play_count_txt.config(state=tk.NORMAL)
            self.play_count_txt.delete(1.0, tk.END)
            self.play_count_txt.insert(tk.END, play_count)
            self.play_count_txt.config(state=tk.DISABLED)

    def add_to_playlist(self):
        filter_by = self.filter_combobox.get()
        input_value = self.video_input_entry.get()

        video_info = read_csv(LIBRARY_CSV_FILE)
        my_info = read_csv(MY_CSV_FILE)

        if input_value == "":
            messagebox.showerror("Input Error", "Video Input fields must be filled out!")
            return
        
        # Check if video exists in video_info
        if filter_by == "ID":
            ids = [key for key, info in video_info.items() if key.lstrip('0') == input_value.lstrip('0')]
        elif filter_by == "Name":
            ids = [key for key, info in video_info.items() if info['name'].strip().lower() == input_value.strip().lower()]
        
        if ids == []:
            messagebox.showerror(f"invalid input", f"Video with {filter_by} {input_value} not found")
            return
        
        id = ids[0]
        if id in my_info:
            messagebox.showerror("Error", "Video already exists in playlist!")
            return
        
        new_video = video_info[id]

        # Add to playlist (MY_DICT_FILE)
        my_info[id] = new_video
        my_info[id]['play_count'] = 0

        write_to_csv(my_info, MY_CSV_FILE, include_play_count=True)
        messagebox.showinfo("Success", "Video added to playlist successfully!")
        self.populate_scrolled_text()

    def update_video(self):
        subprocess.run(["python", "Update_rating.py"])
        
    def on_item_click(self, event):

        my_info = read_csv(MY_CSV_FILE)

        line_start_index = f"@{event.x},{event.y} linestart"
        line_end_index = f"@{event.x},{event.y} lineend"
        line_text = self.list_txt.get(line_start_index, line_end_index)

        try:
            video_id = str(line_text.split(".")[0])
        except ValueError:
            return

        if video_id in my_info:
            self.list_txt.tag_remove("highlight", "1.0", tk.END)
            self.list_txt.tag_add("highlight", line_start_index, line_end_index)
            self.list_txt.tag_config("highlight", background="yellow")

            self.current_video_id = video_id
            self.time_count.set(0)  # Start the video length display at 0
            self.target_video_length = int(my_info[video_id].get('video_length', 0))
            self.video_length.set(self.target_video_length)

            self.video_input_entry.delete(0, tk.END)
            self.check_video(mode="click")
            self.reset_video_length()

    def clear_all(self):

        my_info = read_csv(MY_CSV_FILE)

        if my_info == {}: 
            messagebox.showerror("Error", "No videos in the playlist.")
            return
        
        my_info.clear()
        write_to_csv(my_info, MY_CSV_FILE, include_play_count=True)
        messagebox.showinfo("Success", f"All videos have been deleted.")

        self.video_txt.config(state=tk.NORMAL)
        self.video_txt.delete(1.0, tk.END)
        self.play_count_txt.config(state=tk.NORMAL)
        self.play_count_txt.delete(1.0, tk.END)
        self.current_video_id = None

        self.reset_video_length()
        self.populate_scrolled_text()

    def play_video(self):
        if self.current_video_id is not None and not self.playing:
            self.playing = True
            self.increment_video_length()
            self.increase_play_count()

    def increment_video_length(self):
        if self.playing and self.time_count.get() < self.target_video_length:
            current_video_length = self.time_count.get()
            self.time_count.set(current_video_length + 1)
            
            # Update the progress bar
            self.progress_bar['maximum'] = self.target_video_length
            self.progress_bar['value'] = current_video_length + 1

            self.window.after(1000, self.increment_video_length)

    def reset_video_length(self):
        if self.current_video_id is not None:
            self.playing = False
            self.time_count.set(0)
            self.progress_bar['value'] = 0
            self.play_count_increased = False
    
    def delete_video(self):
        my_info = read_csv(MY_CSV_FILE)
        video_id = self.current_video_id

        if video_id in my_info:
            del my_info[video_id]
            write_to_csv(my_info, MY_CSV_FILE, include_play_count=True)
            self.current_video_id = None
            messagebox.showinfo("Success", f"Deleted video ID {video_id}.")

            self.video_txt.config(state=tk.NORMAL)
            self.video_txt.delete(1.0, tk.END)
            self.play_count_txt.config(state=tk.NORMAL)
            self.play_count_txt.delete(1.0, tk.END)
            
            self.populate_scrolled_text()
        else:
            messagebox.showerror("Error", f"Video ID {video_id} not found in the playlist.")

    def increase_play_count(self):
    
        my_info = read_csv(MY_CSV_FILE)
        video_id = self.current_video_id
    
        if video_id in my_info:
            current_play_count = int(my_info[video_id].get('play_count', 0))
            my_info[video_id]['play_count'] = str(current_play_count + 1)
    
            write_to_csv(my_info, MY_CSV_FILE, include_play_count=True)
            self.play_count_increased = True
            self.check_play_count(self.current_video_id)
        else:
            messagebox.showerror("Error", f"Video ID {video_id} not found in the playlist.")

            
# mainloop
window = tk.Tk()
app = Create_video_lists(window)
fonts.configure()
window.mainloop()