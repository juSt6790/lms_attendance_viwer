from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    # Run your Python script
    result = subprocess.run(['python3', 'attendance.py'], capture_output=True, text=True)
    
    # Get the output from your script
    output = result.stdout
    
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
