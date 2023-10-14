from flask import Flask, request, render_template
import os
import public_vet_code  # Import the file that contains your original code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vet_notes = request.form['vet_notes']
        diagnosis = your_module.get_most_likely_diagnosis(your_module.query_gpt4, vet_notes)  # Replace with the function in your original code
        return render_template('index.html', diagnosis=diagnosis)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
