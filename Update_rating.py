import tkinter as tk
from tkinter import messagebox, ttk
import font_manager as font

# from update_list_and_csv import write_library, update_video_info_and_csv
from read_write_csv import read_csv, write_to_csv

# Define the file where the video dictionary is stored
LIBRARY_CSV_FILE = 'library_video_list.csv'
MY_CSV_FILE = 'my_video_playlist.csv'
video_id = None

            
def lookup_video():
    global video_id
    library = read_csv(LIBRARY_CSV_FILE)

    filter_by = filter_combobox.get()
    lookup_value = lookup_entry.get().strip()

    if not lookup_value:
        messagebox.showerror("Input Error", "Please enter a value to look up!")
        return

    found_video = None

    if filter_by == "ID":
        if lookup_value in library:
            found_video = library[lookup_value]
            video_id = lookup_value
    elif filter_by == "Name":
        for key, video in library.items():
            if video['name'].strip().lower() == lookup_value.strip().lower():
                found_video = video
                video_id = key
                break

    if found_video:
        rating_entry.config(state=tk.NORMAL)
        rating_entry.delete(0, tk.END)
        rating_entry.insert(0, found_video['rating'])
    else:
        messagebox.showinfo("Not Found", "Video not found!")
        rating_entry.config(state=tk.DISABLED)

def modify_rating_and_update():
    global video_id
    new_rating = rating_entry.get().strip()

    if not new_rating:
        messagebox.showerror("Input Error", "Please enter a new rating!")
        return

    try:
        new_rating = float(new_rating)
        if new_rating < 0 or new_rating > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Rating must be a number between 0 and 10!")
        return


    library = read_csv(LIBRARY_CSV_FILE)

    my_video_info = read_csv(MY_CSV_FILE)

    if video_id in library:
        library[video_id]['rating'] = new_rating
        write_to_csv(library, LIBRARY_CSV_FILE)
        messagebox.showinfo("Success", f"Updated rating of video ID {video_id} to {new_rating}.")
        if video_id in my_video_info:
            my_video_info[video_id]['rating'] = new_rating
            write_to_csv(my_video_info, MY_CSV_FILE)

        reset_fields()
    else:
        messagebox.showerror("Error", "Video ID not found in the library!")

def reset_fields():
    lookup_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    rating_entry.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Update Video Rating")

# Create and pack the input fields with labels aligned to the left
tk.Label(root, text="Filter by:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
filter_combobox = ttk.Combobox(root, values=["ID", "Name"])
filter_combobox.grid(row=0, column=1, padx=10, pady=5)
filter_combobox.current(0)

tk.Label(root, text="Lookup Value:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
lookup_entry = tk.Entry(root, width=30)
lookup_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="New Rating:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
rating_entry = tk.Entry(root, width=30)
rating_entry.grid(row=2, column=1, padx=10, pady=5)
rating_entry.config(state=tk.DISABLED)

lookup_button = tk.Button(root, text="Lookup Video", command=lookup_video)
lookup_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

update_button = tk.Button(root, text="Update Rating", command=modify_rating_and_update)
update_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

back_button = tk.Button(root, text="<-- Back", command=root.destroy)
back_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
if __name__ == "__main__":
    font.configure()
    root.mainloop()
