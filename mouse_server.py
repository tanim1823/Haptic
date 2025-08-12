from flask import Flask, request, render_template_string
import pyautogui

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Phone Mouse</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; margin-top: 20px; font-family: Arial; }
        button { width: 40%; height: 60px; margin: 10px; font-size: 20px; }
        canvas { border: 2px solid #555; margin-top: 20px; touch-action: none; }
    </style>
</head>
<body>
    <h1>🖱️ Phone Mouse</h1>

    <!-- Buttons -->
    <form action="/move" method="post">
        <button name="dir" value="up">⬆️</button><br>
        <button name="dir" value="left">⬅️</button>
        <button name="dir" value="right">➡️</button><br>
        <button name="dir" value="down">⬇️</button>
    </form>
    <form action="/click" method="post">
        <button name="btn" value="left">Left Click</button>
        <button name="btn" value="right">Right Click</button>
    </form>
    <form action="/scroll" method="post">
        <button name="scroll" value="up">Scroll Up</button>
        <button name="scroll" value="down">Scroll Down</button>
    </form>

    <!-- Drawing Pad -->
    <h3>Touchpad</h3>
    <canvas id="pad" width="300" height="300"></canvas>

    <script>
        const pad = document.getElementById('pad');
        let ctx = pad.getContext('2d');
        let lastX, lastY;
        let drawing = false;

        function sendMove(dx, dy) {
            fetch('/drag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dx: dx, dy: dy })
            });
        }

        function handleStart(e) {
            e.preventDefault();
            drawing = true;
            const touch = e.touches ? e.touches[0] : e;
            lastX = touch.clientX;
            lastY = touch.clientY;
        }

        function handleMove(e) {
            if (!drawing) return;
            e.preventDefault();
            const touch = e.touches ? e.touches[0] : e;
            const dx = touch.clientX - lastX;
            const dy = touch.clientY - lastY;
            lastX = touch.clientX;
            lastY = touch.clientY;
            sendMove(dx, dy);
        }

        function handleEnd(e) {
            drawing = false;
        }

        pad.addEventListener('mousedown', handleStart);
        pad.addEventListener('mousemove', handleMove);
        pad.addEventListener('mouseup', handleEnd);
        pad.addEventListener('mouseleave', handleEnd);

        pad.addEventListener('touchstart', handleStart);
        pad.addEventListener('touchmove', handleMove);
        pad.addEventListener('touchend', handleEnd);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html)

@app.route('/move', methods=['POST'])
def move():
    direction = request.form['dir']
    x, y = 0, 0
    if direction == 'up':
        y = -20
    elif direction == 'down':
        y = 20
    elif direction == 'left':
        x = -20
    elif direction == 'right':
        x = 20
    pyautogui.moveRel(x, y)
    return home()

@app.route('/click', methods=['POST'])
def click():
    btn = request.form['btn']
    pyautogui.click(button=btn)
    return home()

@app.route('/scroll', methods=['POST'])
def scroll():
    direction = request.form['scroll']
    if direction == 'up':
        pyautogui.scroll(200)
    else:
        pyautogui.scroll(-200)
    return home()

@app.route('/drag', methods=['POST'])
def drag():
    data = request.get_json()
    dx = float(data.get('dx', 0))
    dy = float(data.get('dy', 0))
    pyautogui.moveRel(dx, dy)
    return '', 204  # No content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
