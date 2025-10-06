# Image Filter Web App — Step 1 (Scaffold)

This is the starter scaffold for a Flask + Bootstrap image processing web app.
In Step 1, we set up the folders, a minimal Flask server, and a basic UI shell.

## How to run
1) Create a virtual environment (recommended)

   ### Windows (PowerShell)
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1

   ### macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate

2) Install dependencies
   pip install -r requirements.txt

3) Run the dev server
   python app.py

4) Open the app
   http://127.0.0.1:5000/

## What’s next (Step 2)
- Wire up the upload form
- Save images to `static/uploads`
- Show the uploaded image preview
- Add filter routes & buttons