import tkinter as tk

# Create a new Tkinter window
root = tk.Tk()

# Set the title of the window
root.title("My Application")

# Load the image file using the PhotoImage class
logo_image = tk.PhotoImage(file="image/logo.png")

# Set the logo of the window
root.iconphoto(True, logo_image)

# Create and display the widgets for the application
# ...

# Start the Tkinter event loop
root.mainloop()