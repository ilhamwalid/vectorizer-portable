# Portable Vectorizer AI - Core App (Python + PyQt5)
# Features: Flat-style vectorizer, batch convert, folder output, progress bar, high-res output

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from PIL import Image
import subprocess

class VectorizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vectorizer AI Portable")
        self.setGeometry(200, 200, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Pilih gambar PNG/JPG untuk dikonversi ke SVG (flat style)")
        layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.convert_button = QPushButton("Pilih Gambar & Konversi")
        self.convert_button.clicked.connect(self.select_files)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Pilih Gambar", "", "Images (*.png *.jpg *.jpeg)")
        if not files:
            return
        output_folder = QFileDialog.getExistingDirectory(self, "Pilih Folder Output")
        if not output_folder:
            return

        total = len(files)
        self.progress.setMaximum(total)
        self.progress.setValue(0)

        for i, file_path in enumerate(files):
            try:
                self.convert_to_svg(file_path, output_folder)
                self.progress.setValue(i + 1)
                QApplication.processEvents()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        self.label.setText("Konversi selesai! SVG disimpan di: " + output_folder)

    def convert_to_svg(self, file_path, output_folder):
        filename = os.path.splitext(os.path.basename(file_path))[0]
        temp_resized = os.path.join(output_folder, filename + "_resized.pbm")
        output_svg = os.path.join(output_folder, filename + ".svg")

        # Step 1: Resize to 10000x10000 using Pillow
        with Image.open(file_path) as img:
            img = img.convert("L").resize((10000, 10000))
            img.save(temp_resized, format="PPM")

        # Step 2: Trace using Potrace
        subprocess.run(["potrace", temp_resized, "-s", "-o", output_svg], check=True)
        os.remove(temp_resized)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorizerApp()
    window.show()
    sys.exit(app.exec_())
