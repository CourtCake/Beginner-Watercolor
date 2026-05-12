from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'watercolor_secret_key'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# ── DATA ────────────────────────────────────────────────────────────────────

LESSONS = [
    {
        "id": 1,
        "title": "Wet on Dry",
        "video": "tutorials/technique-1.mp4",
        "description": " This is a simple technique but once this is mastered, it opens up a world of possibilities with watercolor. \n Step 1: Dip your brush in water \n Step 2: Swirl the brush in the paint \n Step 3: Start painting across the paper",
        "best_for": ["Adding details", "Creating sharp edges", "Line work"],
        "tip_title": "Can't get a clean line?",
        "tip": "Too much water. Mix in more paint for more opacity and viscosity, or dab off some water.",
        "image": "wet_on_dry.jpg"
    },
    {
        "id": 2,
        "title": "Wet on Wet",
        "video": "tutorials/technique-2.mp4",
        "description": "Lets build off of the wet on dry technique to create some cool effects using wet paper. \n Step 1: Dip your brush in water and wet brush water onto the watercolor paper \n Step 2: Dip your brush in water and swirl it in the paint \n Step 3: Start painting across the wet areas of the paper",
        "best_for": ["Blending", "Bloom Effect", "Soft backgrounds"],
        "tip_title": "Color going everywhere?",
        "tip": "Too much water on the paper. Put a light wash of water and work in small sections.",
        "image": "wet_on_wet.jpg"
    },
    {
        "id": 3,
        "title": "Flat Wash",
        "video": "tutorials/technique-3.mp4",
        "description": "This technique involves a single color evenly painted and pigmented across the paper \n Step 1: Dip your brush in water \n Step 2: Swirl the brush in the paint \n Step 3: Swirl the paint on the palette to ensure an even coat \n Step 4: Apply the paint to the paper in a smooth, even layers",
        "best_for": ["Blocking out large areas of color"],
        "tip_title": "Can't get an even wash?",
        "tip": "Make sure you are on dry paper and use a palette to mix the desired consistency of paint.",
        "image": "flat_wash.jpg"
    },
    {
        "id": 4,
        "title": "Gradient",
        "video": "tutorials/technique-4.mp4",
        "description": "This technique builds off of the flat wash \n Step 1: Dip your brush in water \n Step 2: Swirl the brush in the paint \n Step 3: Swirl the paint on the palette to ensure an even coat \n Step 4: Apply the paint to the paper in a smooth, even layer \n Step 5: Gradually introduce more water to create a gradient effect.",
        "best_for": ["Ombre effects", "Color blending", "Skies"],
        "tip_title": "Can't get a clean transition?",
        "tip": "Blend harsh areas with a clean brush lightly dipped in water.",
        "image": "gradient.jpg"
    },
    {
        "id": 5,
        "title": "Dry Brush",
        "video": "tutorials/technique-5.mp4",
        "description": "This technique uses a brush with very little paint so that the bristles are still dry and separated. \n Step 1: Dip your brush in a very small amount of water \n Step 2: Swirl the brush in the paint \n Step 3: Brush the paint on dry watercolor paper",
        "best_for": ["Fur", "Grass", "Texture and detail"],
        "tip_title": "Can't get the texture?",
        "tip": "Too much water. Mix in more paint for more opacity or dab off some water.",
        "image": "dry_brush.jpg"
    },
    {
        "id": 6,
        "title": "Wax Crayon",
        "video": "tutorials/technique-6.mp4",
        "description": "This technique masks out areas of the paper. The wax seals the paper, preventing it from absorbing the paint, creating interesting textures. \n Step 1: Use your wax crayon to draw the desired shapes on dry paper \n Step 2: Paint over the desired area with watercolors",
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
        "image": "question_images/question-1.jpg"
    },
    {
        "id": 2,
        "question": "Tom is working on a painting of the night sky and wants to add a full moon and fluffy clouds. What is the best way to achieve this effect?",
        "options": [
            "Outline the moon using a thin wet brush on the dry paper.",
            "Paint the moon first then paint the sky and clouds around them.",
            "Block out the shapes with a thin line using a wax crayon and use wet on wet for clouds.",
            "Paint the sky and clouds first, then use a thick coat of white paint over it."
        ],
        "correct": 2,
        "image": "question_images/question-2.jpg"
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
        "image": "question_images/question-3.jpg"
    },
    {
        "id": 4,
        "question": "Choose the correct techniques for the painting.",
        "options": [
            "Gradient, dry brush, wax crayon",
            "Wet on dry, gradient, flat wash",
            "Wet on wet, wax crayon, flat wash",
            "Wet on wet, wet on dry, gradient"
        ],
        "correct": 2,
        "image": "question_images/question-4.jpg"
    },
    {
        "id": 5,
        "question": "Choose the correct techniques for the painting.",
        "options": [
            "Flat wash, gradient, wet on dry",
            "Wet on dry, wax crayon, wet on wet",
            "Wet on wet, dry brush, gradient",
            "Wet on wet, wet on dry, gradient"
        ],
        "correct": 0,
        "image": "question_images/question-5.jpg"
    }
]

# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    session['start_time'] = datetime.now().isoformat()
    session['lesson_times'] = {}
    session['quiz_answers'] = {}
    session.modified = True
    return redirect(url_for('learn', lesson_num=1))

@app.route('/tutorials/<path:filename>')
def serve_tutorial(filename):
    return send_from_directory('tutorials', filename)

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    if lesson_num < 1 or lesson_num > len(LESSONS):
        return redirect(url_for('home'))
    if 'lesson_times' not in session:
        session['lesson_times'] = {}
    times = session['lesson_times']
    times[str(lesson_num)] = datetime.now().isoformat()
    session['lesson_times'] = times
    session.modified = True

    lesson = LESSONS[lesson_num - 1]
    total = len(LESSONS)
    return render_template('learn.html', lesson=lesson, lesson_num=lesson_num, total=total)

@app.route('/quiz')
def quiz_intro():
    session['quiz_answers'] = {}
    session.modified = True
    return redirect(url_for('quiz', question_num=1))

@app.route('/question_images/<path:filename>')
def serve_question_images(filename):
    return send_from_directory('question_images', filename)

@app.route('/quiz/restart')
def quiz_restart():
    session['quiz_answers'] = {}
    session.modified = True
    return redirect(url_for('quiz', question_num=1))

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
            if answer != '':
                answers[str(question_num)] = int(answer)
            session['quiz_answers'] = answers
            session.modified = True

        if question_num < len(QUIZ_QUESTIONS):
            return redirect(url_for('quiz', question_num=question_num + 1))
        else:
            return redirect(url_for('results'))

    question = QUIZ_QUESTIONS[question_num - 1]
    total = len(QUIZ_QUESTIONS)
    selected = session.get('quiz_answers', {}).get(str(question_num))
    error = request.args.get('error')
    return render_template('quiz.html', question=question, question_num=question_num,
                           total=total, selected=selected,
                           answers=session.get('quiz_answers', {}), error=error)

@app.route('/results')
def results():
    answers = session.get('quiz_answers', {})
    total = len(QUIZ_QUESTIONS)

    unanswered = [i for i in range(1, total + 1) if str(i) not in answers]
    if unanswered:
        nums = ', '.join([f'Question {i}' for i in unanswered])
        return redirect(url_for('quiz', question_num=unanswered[0], error=nums))

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
    return render_template('results.html', score=score, total=total, breakdown=breakdown)

if __name__ == '__main__':
    app.run(debug=True)