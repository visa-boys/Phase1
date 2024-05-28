import tkinter as tk
import numpy as np


class RectangleDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("House Layouts Initializer")
        self.canvas = tk.Canvas(root, width=256, height=256, bg="white")
        self.canvas.pack()
        self.rectangles = []
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.room_options = ["Living room","Master room","Kitchen","Bathroom","Dining room",
              "Child room","Study room","Second room","Guest room","Balcony"]
        self.room_indices = {room: i for i, room in enumerate(self.room_options)}
        self.selected_option = tk.StringVar()
        self.selected_option.set(self.room_options[0])  
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.create_option_buttons()

    def create_option_buttons(self):
        for option in self.room_options:
            button = tk.Radiobutton(self.root, text=option, variable=self.selected_option, value=option)
            button.pack(side=tk.LEFT)

    def on_click(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        self.canvas.delete("rectangle")

        for rect in self.rectangles:
            self.canvas.create_rectangle(rect, outline="black", tags="rectangle")

        self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="black", tags="rectangle"
        )

    def on_release(self, event):
        adjusted_start_x = min(self.start_x, self.end_x)
        adjusted_start_y = min(self.start_y, self.end_y)
        adjusted_end_x = max(self.start_x, self.end_x)
        adjusted_end_y = max(self.start_y, self.end_y)
        selected_room = self.selected_option.get()
        room_index = self.room_indices[selected_room]
        rect_coords = (adjusted_start_x, adjusted_start_y, adjusted_end_x, adjusted_end_y)
        width = abs(adjusted_end_x - adjusted_start_x)
        height = abs(adjusted_end_y - adjusted_start_y)
        arr.append([room_index+2,adjusted_start_x/256.0,adjusted_start_y/256.0,width/256.0,height/256.0])
        print(f"{selected_room} {room_index}: X: {adjusted_start_x}, Y: {adjusted_start_y}, Width: {width}, Height: {height}")
        self.rectangles.append(rect_coords)

if __name__ == "__main__":
    arr=[]
    root = tk.Tk()
    app = RectangleDrawer(root)
    root.mainloop()
    #print(arr)
    np.save('./manual_entry.npy',arr)
