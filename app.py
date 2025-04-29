from flask import *
import spacy
from spacy.matcher import *


print("Loading Spacy..")
nlp = spacy.load("en_core_web_sm")
print("spaCy model loaded.")


SKILLS_LIST = ["Python", "Java", "SQL", "JavaScript", "Communication", "Project Management", "Flask"]

matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

patterns = [nlp.make_doc(text) for text in SKILLS_LIST]


matcher.add("SkillMatcher", patterns)

# ---- Flask ---- #
app = Flask(__name__)


@app.route('/')
def index():
  
  return render_template('index.html')

@app.route('/process', methods=['POST'])

def process_text():
    if not nlp or not matcher:
       return jsonify({"error": "NLP model not initialized"})
    
    if not request.is_json:
        return jsonify({"Error: Request must be JSON"}), 400    
    
    data = request.get_json()
    if 'text' not in data:
       return jsonify({"error": "Missing 'text' key in JSON data"}) , 400

    input_text= data['text']

    if not input_text or input_text.strip() == "":
       return jsonify("error: Text cannot be empty")
    

    print(f"Received text for not processing: {input_text}")

    try:
       
      doc =nlp(input_text)
      matches = matcher(doc)
      
      found_skills = set()
      for match_id, start, end in matches:
        
        skill = doc[start:end].text
        found_skills.add(skill)

      print(f"Found skills: {found_skills}")
    
    except Exception as e:
       
       print(f"Error in processing skills (using nlp)")
       return jsonify({"error": "Failed to process text on server."}), 500


    response_data = {
            "status" : "success",
            "received_text": "input.txt",
            "message": "Text recived, processing logic not implemented"     #part where we add skills
    }

    return jsonify(response_data), 200 #ok code is 200 -----------------IMP
        






if __name__ == '__main__':
  app.run(debug=True)