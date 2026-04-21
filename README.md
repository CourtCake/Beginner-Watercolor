# Beginner Watercolor for Hobbyists — Flask App

## Project Structure
```
watercolor_app/
├── app.py               ← Flask backend (routes + data)
├── requirements.txt
├── templates/
│   ├── base.html        ← Navbar, shared styles
│   ├── home.html        ← Landing page with Start button
│   ├── learn.html       ← Lesson pages  (/learn/<n>)
│   ├── quiz_intro.html  ← Quiz landing  (/quiz)
│   ├── quiz.html        ← Quiz questions (/quiz/<n>)
│   └── results.html     ← Score + breakdown (/results)
└── static/
    └── images/          ← Drop your lesson/quiz images here
```

## Running Locally
```bash
pip install -r requirements.txt
python app.py
# Visit http://127.0.0.1:5000
```

## Adding Your Images
Drop image files into `static/images/` with these names:
- wet_on_dry.jpg
- wet_on_wet.jpg
- flat_wash.jpg
- gradient.jpg
- dry_brush.jpg
- wax_crayon.jpg
- q4_painting.jpg  (the mountain sunset for Q4)
- q5_painting.jpg  (the blue/yellow sky for Q5)

## Git Setup (first time)
```bash
git init
git add .
git commit -m "Initial commit: Flask watercolor app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Routes
| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/start` | Clears session, redirects to lesson 1 |
| `/learn/<n>` | Lesson page (1–6), records timestamp |
| `/quiz` | Quiz intro page |
| `/quiz/<n>` | Quiz question (1–5), stores answer in session |
| `/results` | Score + breakdown |
