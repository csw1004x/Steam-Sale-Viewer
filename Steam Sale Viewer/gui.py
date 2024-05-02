import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen


import requests
import main
def gui_main():
    root = tk.Tk()
    root.title("Steam Sale Viewer")
    root.geometry("1400x1200")
    root.configure(bg="white")
    root.resizable(False, False)

    # Create a title label
    title_label = tk.Label(root, text="Enter the game title you want to search for: (Leave blank to search all)")
    title_label.configure(font=("Courier", 15, "bold"))
    title_label.configure(bg="white")
    title_label.grid(row=100, column=10, padx=155, pady=10)

    # Create an entry for the user to input the game title
    title_entry = tk.Entry(root)
    title_entry.configure(bg="white")
    title_entry.configure(font=("Courier", 15))
    title_entry.grid(row=200, column=10, padx=10, pady=10)

    # Create a search button
    search_button = tk.Button(root, text="Search", command=lambda: get_user_input(title_entry, root, frame, canvas))
    search_button.configure(bg="white")
    search_button.configure(font=("Courier", 15, "bold"))
    search_button.grid(row=300, column=10, padx=10, pady=10)

    # Create a canvas
    canvas = tk.Canvas(root)
    canvas.configure(bg="white")
    canvas.grid(row=600, column=10, padx=10, pady=10)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=600, column=11, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the game data
    frame = tk.Frame(canvas)
    frame.configure(bg="white")
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Resize the canvas and frame to fit the window
    canvas.configure(width=1300, height=1000)
    frame.configure(width=800, height=800)

    root.mainloop()

def show_game_data(game_data, root, frame, canvas):
    # Clear the canvas before showing new game data
    canvas.delete("all")
    # Create a scrollable frame inside the canvas
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.configure(bg="white")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure the canvas to resize with the frame
    scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    # Add the game data to the scrollable frame
    index = 0 
    for i, game in enumerate(game_data):
        image_url = game['image_link']

        data = urlopen(image_url)
        image = ImageTk.PhotoImage(data=data.read())
        image_label = tk.Label(scrollable_frame, image=image)
        image_label.image = image
        image_label.grid(row=index, column=0, padx=5, pady=5, sticky="w")

        title = game['title']
        title_label = tk.Label(scrollable_frame, text=title)
        title_label = tk.Label(scrollable_frame, text=game['title'])
        title_label.configure(font=("Courier", 18, "bold"))
        title_label.configure(bg="white")
        title_label.grid(row=index, column=1, padx=5, pady=5, sticky="w")

        

        price = game['original_price']
        price = price.split(" ")
        price[0] = price[0].replace("C$", "")
        price[2] = "C$" + price[2]
        price = price[0] + " " + price[2]
        original_price_label = tk.Label(scrollable_frame, text=price)
        original_price_label.configure(font=("Courier", 13, "bold"))
        original_price_label.configure(bg="white")
        original_price_label.grid(row=index, column=1, padx=5, pady=5, sticky="e")  # Adjusted column to 1 and sticky to "e"
    

        release_date_label = tk.Label(scrollable_frame, text=game['release_date'])
        release_date_label.configure(font=("Courier", 13, "bold"))
        release_date_label.configure(bg="white")
        release_date_label.grid(row=index + 1, column=0, padx=5, pady=5, sticky="w")

        review_summary = game['review_summary'].replace("<br>", ": ")
        review_summary_label = tk.Label(scrollable_frame, text=review_summary)
        review_summary_label.configure(font=("Courier", 13, "bold"))

        if "Negative" in review_summary:
            review_summary_label.configure(fg="red")
        elif "Mixed" in review_summary:
            review_summary_label.configure(fg="orange")
        else:
            review_summary_label.configure(fg="green")

        review_summary_label.configure(bg="white")
        review_summary_label.grid(row=index + 1, column=1, padx=5, pady=5, sticky="w")

        # Create a separator line between games
        separator = tk.Frame(scrollable_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.grid(row=index + 2, column=0, columnspan=3, sticky="we", padx=5, pady=5)

        index = index + 3
        root.update_idletasks()

    # Scroll to the top of the canvas
    canvas.yview_moveto(0)
    
def get_user_input(title_entry, root, frame, canvas):
    # Clear the frame before showing new game data
    frame.destroy()
    frame = tk.Frame(canvas)
    frame.configure(bg="white")
    canvas.create_window((0, 0), window=frame, anchor="nw")
    root.update()

    user_input = title_entry.get()
    list_game = main.scrape_steam_sale(user_input)
    show_game_data(list_game, root, frame, canvas)