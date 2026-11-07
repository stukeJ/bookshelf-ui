Display for a bookshelf screen that shows your current progress for the book

Works on pc and touchscreen raspberry pi display

---

Enter the page amount of your book and you can see your progress by updating the page you are on
When unused for 15 seconds, display will turn black and only show a progress bar

---

On windows:
pip install -r requirements.txt
python main.py
```

---

On raspberry pi:

```bash
# Tkinter libraries
sudo apt update
sudo apt install -y python3-tk python3-pil python3-pil.imagetk

# Create virtual environment and install requirements
cd ~/kirjateline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start up
python3 main.py
```
If you use an older Python 3.7.3 -version: `pip install "customtkinter<=5.1.3" "pillow<10.0.0"`)*
