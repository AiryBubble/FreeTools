from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageOps, ImageChops

SIZE = 460

class CircleCropApp:
    def __init__(self, root):
        self.root = root
        root.title("円形透過 PNG ツール")
        root.resizable(False, False)
        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.result = tk.StringVar(value="待機中")
        frame = ttk.Frame(root, padding=16)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="入力ファイル").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(frame, textvariable=self.input_path, width=48).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Button(frame, text="選択", command=self.choose_input).grid(row=0, column=2, padx=(8, 0), pady=6)
        ttk.Label(frame, text="出力先フォルダ").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(frame, textvariable=self.output_dir, width=48).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Button(frame, text="選択", command=self.choose_output).grid(row=1, column=2, padx=(8, 0), pady=6)
        ttk.Button(frame, text="実行", command=self.run, width=18).grid(row=2, column=0, columnspan=3, pady=(14, 8))
        ttk.Label(frame, text="実行結果").grid(row=3, column=0, sticky="nw", padx=(0, 10), pady=6)
        ttk.Label(frame, textvariable=self.result, wraplength=460, justify="left").grid(row=3, column=1, columnspan=2, sticky="w", pady=6)

    def choose_input(self):
        path = filedialog.askopenfilename(title="入力画像を選択", filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp"), ("すべてのファイル", "*.*")])
        if path:
            self.input_path.set(path)
            if not self.output_dir.get():
                self.output_dir.set(str(Path(path).parent))

    def choose_output(self):
        path = filedialog.askdirectory(title="出力先フォルダを選択")
        if path:
            self.output_dir.set(path)

    def run(self):
        source = Path(self.input_path.get().strip())
        destination = Path(self.output_dir.get().strip())
        if not source.is_file():
            self.result.set("入力ファイルを選択してください。")
            return
        if not destination.is_dir():
            self.result.set("有効な出力先フォルダを選択してください。")
            return
        output = destination / f"{source.stem}_circle.png"
        try:
            with Image.open(source) as original:
                image = ImageOps.exif_transpose(original).convert("RGBA")
                image.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
                canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
                x, y = (SIZE - image.width) // 2, (SIZE - image.height) // 2
                canvas.alpha_composite(image, (x, y))
                mask = Image.new("L", (SIZE, SIZE), 0)
                ImageDraw.Draw(mask).ellipse((0, 0, SIZE - 1, SIZE - 1), fill=255)
                canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), mask))
                canvas.save(output, format="PNG")
            self.result.set(f"完了: {output}")
        except Exception as exc:
            self.result.set(f"失敗: {exc}")

if __name__ == "__main__":
    root = tk.Tk()
    CircleCropApp(root)
    root.mainloop()
