import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO


class FoxApp:
    def __init__(self, app_root):
        self.root = app_root
        self.root.title("Генератор лисичек")
        self.root.geometry("450x500")

        self.session = requests.Session()

        self.frame = ttk.Frame(app_root, padding=10)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.image_label = ttk.Label(self.frame, text="Загрузка...", anchor="center")
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        self.btn = ttk.Button(self.frame, text="Следующая лисичка", command=self.update_image)
        self.btn.grid(row=1, column=0, padx=10, pady=10)

        self.photo = None
        self.current_image_url = None

        self.update_image()

    def get_fox_image(self):
        try:
            response = self.session.get("https://randomfox.ca/floof/", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("image", None)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def update_image(self):
        self.image_label.config(text="Загрузка...")

        try:
            image_url = self.get_fox_image()
            if not image_url:
                self.image_label.config(text="Ошибка загрузки")
                return

            if image_url == self.current_image_url:
                return

            response = self.session.get(image_url, timeout=5)
            response.raise_for_status()

            img_data = Image.open(BytesIO(response.content))
            img_data.thumbnail((400, 400))

            self.photo = ImageTk.PhotoImage(img_data)
            self.image_label.config(image=self.photo, text="")
            self.current_image_url = image_url

        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image_label.config(text="Ошибка загрузки")


if __name__ == "__main__":
    root = tk.Tk()
    app = FoxApp(root)
    root.mainloop()
