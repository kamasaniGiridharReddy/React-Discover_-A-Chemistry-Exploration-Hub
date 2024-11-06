from flask import Flask, render_template, request
from groq import Groq  # type: ignore

app = Flask(__name__)

# Groq API key configuration
GROQ_API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=GROQ_API_KEY)

# Function to fetch element information
def get_element_information(element_symbol):
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"Provide general information on the element with the symbol {element_symbol}."
        }],
        model="gemma2-9b-it",
    )
    return response.choices[0].message.content

# Function to suggest compounds
def get_possible_compounds(element1, element2):
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"Suggest compounds that can be formed using elements {element1} and {element2}."
        }],
        model="gemma2-9b-it",
    )
    return response.choices[0].message.content

# Function to describe reactions
def get_reaction_info(compound1, compound2):
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"Describe a reaction between {compound1} and {compound2}."
        }],
        model="gemma2-9b-it",
    )
    return response.choices[0].message.content



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/element_info', methods=['GET', 'POST'])
def element_info():
    element_info_content = ""
    if request.method == 'POST':
        element_symbol = request.form.get('element_symbol')
        element_info_content = get_element_information(element_symbol)
    return render_template('element_info.html', element_info=element_info_content)

@app.route('/compound_formation', methods=['GET', 'POST'])
def compound_formation():
    compound_content = ""
    if request.method == 'POST':
        element1 = request.form.get('element1')
        element2 = request.form.get('element2')
        compound_content = get_possible_compounds(element1, element2)
    return render_template('compound_formation.html', compound_content=compound_content)

@app.route('/reaction_info', methods=['GET', 'POST'])
def reaction_info():
    reaction_content = ""
    if request.method == 'POST':
        compound1 = request.form.get('compound1')
        compound2 = request.form.get('compound2')
        reaction_content = get_reaction_info(compound1, compound2)
    return render_template('reaction_info.html', reaction_content=reaction_content)

@app.route('/compound_cost', methods=['GET', 'POST'])
def compound_cost():
    cost_content = ""
    if request.method == 'POST':
        compound_name = request.form.get('compound_name')
        cost_content = get_estimated_cost(compound_name)
    return render_template('compound_cost.html', cost_content=cost_content)

if __name__ == '__main__':
    app.run(debug=True)
