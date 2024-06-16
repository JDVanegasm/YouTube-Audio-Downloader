import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from script import download_wav_audio

def choose_directory():
    """Opens a dialog to choose the download directory"""
    directory = filedialog.askdirectory(title="Choose download Directory")
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def start_download():
    """Starts the download process"""
    url = url_entry.get()
    name = name_entry.get()
    directory = directory_entry.get()

    if not url:
        messagebox.showerror("Error", "You must enter the URL of the content.")
        return
    if not name:
        messagebox.showerror("Error", "You must enter the name of the content.")
        return
    if not directory:
        messagebox.showerror("Error", "You must select the download directory.")
        return

    download_address = f"{directory}/{name}"
    try:
        download_wav_audio(url, download_address, progress_callback=update_progress_bar)
        messagebox.showinfo("Success!", f"The audio file has been saved to: {download_address}.wav")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading audio: {str(e)}")

def clean_fields():
    """Clears the input fields"""
    url_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    directory_entry.delete(0, tk.END)
    progress_var.set(0)

def update_progress_bar(stream=None, chunk=None, bytes_remaining=None):
    """Updates the progress bar during the download"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    root.update_idletasks()

# Create the main window
root = tk.Tk()
root.title("Download YouTube Audio")
root.geometry("500x400")
root.resizable(False, False)

# Widget styles
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TEntry', font=('Helvetica', 12))

# Create and place widgets
ttk.Label(root, text="Content URL:").pack(pady=5)
url_entry = ttk.Entry(root, width=60)
url_entry.pack(pady=5)

ttk.Label(root, text="File name:").pack(pady=5)
name_entry = ttk.Entry(root, width=60)
name_entry.pack(pady=5)

ttk.Label(root, text="Download Directory:").pack(pady=5)
directory_entry = ttk.Entry(root, width=60)
directory_entry.pack(pady=5)

ttk.Button(root, text="Choose Directory", command=choose_directory).pack(pady=5)

# Create a frame for buttons and adjust margins
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Download", command=start_download).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Clean fields", command=clean_fields).pack(side=tk.LEFT, padx=10)

# Progress bar
progress_var = tk.DoubleVar()
ttk.Progressbar(root, variable=progress_var, maximum=100).pack(pady=10, fill=tk.X, padx=20)

# Start the application
root.mainloop()