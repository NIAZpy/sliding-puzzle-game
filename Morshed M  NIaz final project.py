import tkinter as tk
from PIL import Image, ImageTk
import random
import winsound

SIZE = 3

IMAGE_PATHS = [
    "code in palce/bird.jpg",
    "code in palce/fish.jpg",
    "code in palce/rabbit.jpeg",
    "code in palce/snake.jpg"
]


# ---------------------------------------------------------
# PUZZLE WINDOW
# ---------------------------------------------------------
class SlidingPuzzleWindow:
    def __init__(self, img_path):
        self.win = tk.Toplevel()
        self.win.title("Sliding Puzzle")
        self.win.configure(bg="#fff0fa")

        self.image = Image.open(img_path).resize((600, 600))
        self.pw = self.image.width // SIZE
        self.ph = self.image.height // SIZE

        self.tiles = []
        self.board = []
        self.empty = (SIZE - 1, SIZE - 1)

        self.cut_image()
        self.create_board()
        self.create_ui()

    def cut_image(self):
        for r in range(SIZE):
            row_tiles = []
            for c in range(SIZE):
                if r == SIZE - 1 and c == SIZE - 1:
                    row_tiles.append(None)
                    continue
                piece = self.image.crop((c*self.pw, r*self.ph, (c+1)*self.pw, (r+1)*self.ph))
                row_tiles.append(ImageTk.PhotoImage(piece))
            self.tiles.append(row_tiles)

    def create_board(self):
        nums = list(range(SIZE*SIZE - 1))
        while True:
            random.shuffle(nums)
            if self.is_solvable(nums):
                break

        k = 0
        for r in range(SIZE):
            row = []
            for c in range(SIZE):
                if r == SIZE - 1 and c == SIZE - 1:
                    row.append(None)
                else:
                    row.append(nums[k])
                    k += 1
            self.board.append(row)

    def is_solvable(self, arr):
        inv = 0
        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0

    def create_ui(self):
        self.buttons = []
        for r in range(SIZE):
            row_btns = []
            for c in range(SIZE):
                val = self.board[r][c]
                if val is None:
                    btn = tk.Button(self.win, state="disabled", relief="flat", bg="#fff0fa")
                else:
                    tr, tc = val // SIZE, val % SIZE
                    img = self.tiles[tr][tc]

                    btn = tk.Button(
                        self.win,
                        image=img,
                        relief="raised",
                        bd=4,
                        highlightthickness=2,
                        highlightbackground="#ff69b4",
                        bg="#fff0fa",
                        command=lambda rr=r, cc=c: self.move(rr, cc)
                    )
                    btn.image = img

                btn.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def move(self, r, c):
        er, ec = self.empty

        if (abs(er - r) == 1 and ec == c) or (abs(ec - c) == 1 and er == r):

            winsound.PlaySound("slide.wav", winsound.SND_ASYNC)

            self.board[er][ec], self.board[r][c] = self.board[r][c], self.board[er][ec]
            self.empty = (r, c)

            self.update_ui()

            if self.check_win():
                self.show_win()

    def update_ui(self):
        for r in range(SIZE):
            for c in range(SIZE):
                val = self.board[r][c]
                btn = self.buttons[r][c]

                if val is None:
                    btn.config(image="", state="disabled", relief="flat")
                else:
                    tr, tc = val // SIZE, val % SIZE
                    img = self.tiles[tr][tc]

                    btn.config(
                        image=img,
                        state="normal",
                        relief="raised",
                        bd=4,
                        highlightthickness=2,
                        highlightbackground="#ff69b4",
                        command=lambda rr=r, cc=c: self.move(rr, cc)
                    )
                    btn.image = img

    def check_win(self):
        correct = list(range(SIZE*SIZE - 1))
        flat = []

        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] is not None:
                    flat.append(self.board[r][c])

        return flat == correct

    def show_win(self):
        win = tk.Toplevel(self.win)
        win.title("🎉 Game Over 🎉")
        win.configure(bg="#ffe6ff")

        title = tk.Label(
            win,
            text="🌟✨ YOU DID IT! ✨🌟",
            font=("Comic Sans MS", 28, "bold"),
            fg="#0F746B",
            bg="#595F59",
        )
        title.pack(pady=20)

        msg = tk.Label(
            win,
            text="🎀 Amazing! You solved the puzzle! 🎀\n\n🌸 Great job, superstar! 🌸",
            font=("Comic Sans MS", 18),
            fg="#584c9c",
            bg="#ffe6ff",
            justify="center"
        )
        msg.pack(pady=10)

        ok_btn = tk.Button(
            win,
            text="💖 OK 💖",
            font=("Comic Sans MS", 18, "bold"),
            fg="white",
            bg="#6cf199",
            activebackground="#c4a74a",
            relief="raised",
            bd=6,
            padx=20,
            pady=5,
            command=win.destroy
        )
        ok_btn.pack(pady=20)

        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (w // 2)
        y = (win.winfo_screenheight() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")


# ---------------------------------------------------------
# MAIN MENU WITH THUMBNAILS
# ---------------------------------------------------------
class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puzzle Menu")
        self.root.geometry("750x750")
        self.root.configure(bg="#fff0fa")

        self.current_puzzle = None

        tk.Label(
            self.root,
            text="🌈 Choose Your Puzzle 🌈",
            font=("Comic Sans MS", 26, "bold"),
            fg="#308657",
            bg="#fff0fa"
        ).pack(pady=20)

        self.frame = tk.Frame(self.root, bg="#fff0fa")
        self.frame.pack()

        self.load_thumbnails()

        self.root.mainloop()

    def load_thumbnails(self):
        self.thumbs = []

        for i, path in enumerate(IMAGE_PATHS):
            img = Image.open(path).resize((150, 150))
            thumb = ImageTk.PhotoImage(img)
            self.thumbs.append(thumb)

            box = tk.Frame(self.frame, padx=20, pady=20, bg="#74ac5f")
            box.grid(row=i//2, column=i%2)

            tk.Label(box, image=thumb, bg="#fff0fa").pack()

            tk.Button(
                box,
                text=f"💝 Puzzle {i+1} 💝",
                font=("Comic Sans MS", 16, "bold"),
                fg="white",
                bg="#e62121",
                activebackground="#6e0d41",
                relief="raised",
                bd=6,
                width=15,
                command=lambda p=path: self.open_puzzle(p)
            ).pack(pady=10)

    def open_puzzle(self, img_path):
        if self.current_puzzle is not None:
            try:
                self.current_puzzle.win.destroy()
            except:
                pass

        self.current_puzzle = SlidingPuzzleWindow(img_path)


if __name__ == "__main__":
    MainMenu()
