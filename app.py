from flask import Flask, render_template, redirect, url_for, request, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'watercolor_secret_key'

# ── DATA ────────────────────────────────────────────────────────────────────

LESSONS = [
    {
        "id": 1,
        "title": "Wet on Dry",
        "description": "Just get your brush wet, load it up with paint until it reaches the desired consistency and opacity, and start painting on the dry paper.",
        "best_for": ["Adding details", "Creating sharp edges", "Line work"],
        "tip_title": "Can't get a clean line?",
        "tip": "Too much water. Mix in more paint for more opacity and viscosity, or dab off some water.",
        "image": "wet_on_dry.jpg"
    },
    {
        "id": 2,
        "title": "Wet on Wet",
        "description": "Similar to wet on dry, but before painting you add a wash of water to the paper. This creates a softer, diffused effect. You can also use this to create a bloom effect and other fluid textures.",
        "best_for": ["Blending", "Bloom Effect", "Soft backgrounds"],
        "tip_title": "Color going everywhere?",
        "tip": "Too much water on the paper. Put a light wash of water and work in small sections.",
        "image": "wet_on_wet.jpg"
    },
    {
        "id": 3,
        "title": "Flat Wash",
        "description": "A single color evenly painted and pigmented across the paper. Prepare a large puddle of paint on the palette and use a square brush on dry paper.",
        "best_for": ["Blocking out large areas of color"],
        "tip_title": "Can't get an even wash?",
        "tip": "Make sure you are on dry paper and use a palette to mix the desired consistency of paint.",
        "image": "flat_wash.jpg"
    },
    {
        "id": 4,
        "title": "Gradient",
        "description": "Starts just like a flat wash, but every pass you introduce a bit more water to diffuse the color. This creates a gradual ombre effect and can also blend one color into another.",
        "best_for": ["Ombre effects", "Color blending", "Skies"],
        "tip_title": "Can't get a clean transition?",
        "tip": "Blend harsh areas with a clean brush lightly dipped in water.",
        "image": "gradient.jpg"
    },
    {
        "id": 5,
        "title": "Dry Brush",
        "description": "Use a brush with very little paint so that the bristles are still dry and separated. Lightly and quickly stroke the dry paper.",
        "best_for": ["Fur", "Grass", "Texture and detail"],
        "tip_title": "Can't get the texture?",
        "tip": "Too much water. Mix in more paint for more opacity or dab off some water.",
        "image": "dry_brush.jpg"
    },
    {
        "id": 6,
        "title": "Wax Crayon",
        "description": "This technique masks out areas of the paper. The wax seals the paper, preventing it from absorbing the paint, creating interesting textures.",
        "best_for": ["Blocking areas", "Intricate line work"],
        "tip_title": "Finding this tricky?",
        "tip": "Think about your goal. Use thin lines if you want to paint inside the blocked area.",
        "image": "wax_crayon.jpg"
    }
]

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Jacob wants to create a soft vignette gradient around the edge of the paper. What is the best way to achieve this effect?",
        "options": [
            "Load up the brush with paint and feather it across the edges",
            "Use the wet on wet technique to diffuse the color softly, focusing color on the edge.",
            "Use the flat brush technique to outline the paper then dab water along the edges.",
            "Paint the entire page in the main color then from the center brush out white paint."
        ],
        "correct": 1,
        "image": None
    },
    {
        "id": 2,
        "question": "Tom is working on a painting of the night sky and wants to add a full moon and white fluffy clouds. What is the best way to achieve this effect?",
        "options": [
            "Outline the area using a thin wet brush on the dry paper.",
            "Paint those parts first then paint the sky parts around them.",
            "Block out the area with a thin line using a wax crayon.",
            "Paint the sky first then use a thick coat of white paint over it."
        ],
        "correct": 2,
        "image": None
    },
    {
        "id": 3,
        "question": "Austin wants to paint a grassy field. What is the best way to achieve this effect?",
        "options": [
            "Use the corner of a wide brush and make a lot of thin strokes.",
            "Flat wash the field with green then use a detail brush with white for detail.",
            "Use a wax crayon to make blades of grass then flat wash with green.",
            "Use a mix of dry brush strokes and a detail brush to add depth and texture."
        ],
        "correct": 3,
        "image": None
    },
    {
        "id": 4,
        "question": "Choose the correct techniques for the painting.",
        "options": [
            "Gradient, dry brush, wax crayon.",
            "Wet on dry, gradient, flat wash.",
            "Wet on wet, wax crayon, flat wash."
        ],
        "correct": 2,
        "image": "q4_painting.jpg"
    },
    {
        "id": 5,
        "question": "Choose the correct techniques for the painting.",
        "options": [
            "Flat wash, gradient, wet on dry.",
            "Wet on dry, wax crayon, wet on wet.",
            "Wet on wet, dry brush, gradient."
        ],
        "correct": 0,
        "image": "q5_painting.jpg"
    }
]

# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    session.clear()
    return render_template('home.html')

@app.route('/start')
def start():
    session['start_time'] = datetime.now().isoformat()
    session['lesson_times'] = {}
    session['quiz_answers'] = {}
    return redirect(url_for('learn', lesson_num=1))

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    if lesson_num < 1 or lesson_num > len(LESSONS):
        return redirect(url_for('home'))
    # Record time user entered this lesson page
    if 'lesson_times' not in session:
        session['lesson_times'] = {}
    times = session['lesson_times']
    times[str(lesson_num)] = datetime.now().isoformat()
    session['lesson_times'] = times

    lesson = LESSONS[lesson_num - 1]
    total = len(LESSONS)
    return render_template('learn.html', lesson=lesson, lesson_num=lesson_num, total=total)

@app.route('/quiz')
def quiz_intro():
    return render_template('quiz_intro.html')

@app.route('/quiz/<int:question_num>', methods=['GET', 'POST'])
def quiz(question_num):
    if question_num < 1 or question_num > len(QUIZ_QUESTIONS):
        return redirect(url_for('home'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer is not None:
            if 'quiz_answers' not in session:
                session['quiz_answers'] = {}
            answers = session['quiz_answers']
            answers[str(question_num)] = int(answer)
            session['quiz_answers'] = answers

        if question_num < len(QUIZ_QUESTIONS):
            return redirect(url_for('quiz', question_num=question_num + 1))
        else:
            return redirect(url_for('results'))

    question = QUIZ_QUESTIONS[question_num - 1]
    total = len(QUIZ_QUESTIONS)
    selected = session.get('quiz_answers', {}).get(str(question_num))
    return render_template('quiz.html', question=question, question_num=question_num,
                           total=total, selected=selected)

@app.route('/results')
def results():
    answers = session.get('quiz_answers', {})
    score = 0
    breakdown = []
    for q in QUIZ_QUESTIONS:
        user_ans = answers.get(str(q['id']))
        correct = (user_ans == q['correct'])
        if correct:
            score += 1
        breakdown.append({
            'question': q['question'],
            'your_answer': q['options'][user_ans] if user_ans is not None else 'No answer',
            'correct_answer': q['options'][q['correct']],
            'correct': correct
        })
    total = len(QUIZ_QUESTIONS)
    return render_template('results.html', score=score, total=total, breakdown=breakdown)

if __name__ == '__main__':
    app.run(debug=True)
