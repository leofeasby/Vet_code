from flask import Flask, request, render_template
import os
import public_vet_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vet_notes = request.form['vet_notes']  # Fetching vet notes from form
        gpt4_output = public_vet_code.query_gpt4(f"As a clinical vet, list only the 1 most relevant filename of the diagnostic categories that should be examined for a case with the following symptoms: {vet_notes}.")  # Query GPT-4 to get the relevant filename
        diagnosis = public_vet_code.get_most_likely_diagnosis(gpt4_output, vet_notes)  # Now pass both gpt4_output and vet_notes
        return render_template('index.html', diagnosis=diagnosis)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
