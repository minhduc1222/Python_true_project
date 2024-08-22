import tkinter as tk
from tkinter import ttk, messagebox as messagebox
import subprocess
import tkinter.scrolledtext as tkst
import font_manager as fonts
from read_write_csv import read_csv, write_to_csv

LIBRARY_CSV_FILE = 'library_video_list.csv'

class CheckVideos():
    def __init__(self, window):
        self.window = window
        window.geometry("1000x400")  # Set the window size
        window.title("Check Videos")  # Set the window title

        self.current_video_id = None  # Initialize the current video ID as None
        self.create_widgets()  # Call the function to create the widgets
        self.list_all_videos()  # List all videos on initialization

    def create_widgets(self):
        # Filter widgets
        self.filter_label = tk.Label(self.window, text="Filter by:")  # Label for filter
        self.filter_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

        self.filter_combobox = ttk.Combobox(self.window, width=12, values=["ID", "Name", "Video Length", "Rating", "Director"])
        self.filter_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        self.filter_combobox.current(0)  # Default to the first item (ID)

        # List all videos button
        list_videos_btn = tk.Button(self.window, text="List All Videos", command=self.list_all_videos)
        list_videos_btn.grid(row=0, column=2, padx=10, pady=10)

        # Add video button
        add_video_btn = tk.Button(self.window, text="Add Video", command=self.add_video)
        add_video_btn.grid(row=0, column=3, padx=10, pady=10)

        # Delete video button
        delete_video_btn = tk.Button(self.window, text="Delete Video", command=self.delete_video)
        delete_video_btn.grid(row=1, column=6, padx=10, pady=10)

        # Enter video number label and entry
        enter_lbl = tk.Label(self.window, text="Enter ")
        enter_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="E")

        self.filter_entry = tk.Entry(self.window, width=25)
        self.filter_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.filter_entry.bind("<KeyRelease>", self.apply_filter)  # Bind key release event to filter

        # ScrolledText widget for listing videos
        self.list_txt = tkst.ScrolledText(self.window, width=60, height=12, cursor="arrow", state=tk.DISABLED)
        self.list_txt.grid(row=2, column=0, columnspan=4, rowspan=4, sticky="W", padx=10, pady=10)
        self.list_txt.bind("<Button-1>", self.on_item_click)  # Bind click event to select video

        # Text widget to display video details
        self.video_txt = tk.Text(self.window, width=24, height=4, wrap="none", state=tk.DISABLED)
        self.video_txt.grid(row=2, column=4, columnspan=3, sticky="NW", padx=10, pady=10)

        # Configure ScrolledText to hide the cursor
        self.list_txt.config(insertbackground=self.list_txt.cget("background"))

        # Create video list button
        self.create_video_list_btn = tk.Button(self.window, text="Create Video List", command=self.create_video_list)
        self.create_video_list_btn.grid(row=0, column=4, columnspan=3, padx=10, pady=10)

        # Back button to close the window
        back_btn = tk.Button(self.window, text="<-- Back", command=self.window.destroy)
        back_btn.grid(row=0, column=7, padx=10, pady=10, sticky="E")

    def adding_dot_zero_if_integer(self, value):
        # Ensure that integer values are formatted with a .0 (e.g., 8 -> 8.0)
        return f"{value}.0" if isinstance(value, int) else value
    
    def populate_scrolled_text(self, filter_value=None, filter_by="ID"):
        data = read_csv(LIBRARY_CSV_FILE)  # Read video data from the CSV file
        self.list_txt.config(state=tk.NORMAL)  # Enable the ScrolledText widget for editing
        self.list_txt.delete(1.0, tk.END)  # Clear the ScrolledText widget
        for video_id, details in data.items():
            # Display video details based on the selected filter criteria
            if filter_value is None:
                self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
            else:
                if filter_by == "ID" and video_id == filter_value:
                    self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
                elif filter_by == "Name" and filter_value.lower() in details['name'].lower():
                    self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
                elif filter_by == "Video Length" and int(details['video_length']) == filter_value:
                    self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
                elif filter_by == "Rating" and float(details['rating']) == self.adding_dot_zero_if_integer(filter_value):
                    self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
                elif filter_by == "Director" and filter_value.lower() in details['director'].lower():
                    self.list_txt.insert(tk.END, f"{video_id}. {details['name']}\n")
        self.list_txt.config(state=tk.DISABLED)  # Disable the ScrolledText widget after editing
        
    def list_all_videos(self):
        self.filter_entry.delete(0, tk.END)  # Clear the filter entry
        self.populate_scrolled_text()  # List all videos

    def apply_filter(self, event):
        # Apply the filter based on user input
        filter_by = self.filter_combobox.get()  # Get selected filter criteria
        filter_value = self.filter_entry.get()  # Get entered filter value

        # Convert filter value to the appropriate type based on the selected filter criteria
        if filter_by in ["ID", "Name", "Director"]:
            filter_value = str(filter_value) if filter_value else None
        elif filter_by == "Video Length":
            try:
                filter_value = int(filter_value)
            except ValueError:
                filter_value = None
        elif filter_by == "Rating":
            try:
                filter_value = float(filter_value)
            except ValueError:
                filter_value = None

        self.populate_scrolled_text(filter_value, filter_by)  # Update the list based on the filter

    def check_video(self):
        data = read_csv(LIBRARY_CSV_FILE)  # Read video data from the CSV file

        if self.current_video_id is not None:
            details = data.get(self.current_video_id, {})  # Get details of the selected video
            if details:
                # Display video details in the Text widget
                video_details = (f"Name: {details['name']}\n"
                                 f"Video Length: {details['video_length']}\n"
                                 f"Rating: {details['rating']}\n"
                                 f"Director: {details['director']}\n")
                self.video_txt.config(state=tk.NORMAL)
                self.video_txt.delete(1.0, tk.END)
                self.video_txt.insert(tk.END, video_details)
                self.video_txt.config(state=tk.DISABLED)

    def on_item_click(self, event):
        # Handle click event to select a video
        data = read_csv(LIBRARY_CSV_FILE)

        # Get the line of text where the click occurred
        line_start_index = self.list_txt.index(f"@{event.x},{event.y} linestart")
        line_end_index = self.list_txt.index(f"@{event.x},{event.y} lineend")
        line_text = self.list_txt.get(line_start_index, line_end_index)


        # Try to extract the video ID from the line_text
        video_id = line_text.split(".")[0]  # Assuming video_id is the first item in the line_text
    
        if video_id in data:
            # Highlight the selected video
            self.list_txt.tag_remove("highlight", "1.0", tk.END)
            self.list_txt.tag_add("highlight", line_start_index, line_end_index)
            self.list_txt.tag_config("highlight", background="yellow")
    
            self.current_video_id = video_id
    
            # Find the corresponding video data
            self.check_video()

    def add_video(self):
        subprocess.run(["python", "Add_new_video.py"])  # Run the script to add a new video
        self.list_all_videos()  # Refresh the video list
        
    def delete_video(self):
        data = read_csv(LIBRARY_CSV_FILE)  # Read video data from the CSV file
        if self.current_video_id is None:
            messagebox.showerror("Error", "No video selected!")  # Show error if no video is selected
            return
        
        if self.current_video_id in data:
            del data[self.current_video_id]  # Delete the selected video
            write_to_csv(data, LIBRARY_CSV_FILE)  # Write the updated data back to the CSV file
            self.list_all_videos()  # Refresh the video list
            messagebox.showinfo("Success", f"Deleted video with key {self.current_video_id}.")
        else:
            messagebox.showerror("Error", "Video not found!")  # Show error if the video is not found

    def create_video_list(self):
        subprocess.run(["python", "Create_video_list.py"])  # Run the script to create a video list

if __name__ == "__main__":
    window = tk.Tk()
    app = CheckVideos(window)
    fonts.configure()  # Configure the fonts
    window.mainloop()  # Run the Tkinter main loop
