from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
from models.parser import parse_user_intent
from models.generator import generate_yaml
from models.refiner import parse_refinement_intent, apply_refinement
from validation.validator import validate_yaml

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/api/generate-yaml', methods=['POST'])
def generate_yaml_endpoint():
    user_text = request.json.get('text', '')
    
    # Process the text through our pipeline
    parsed_requirements = parse_user_intent(user_text)
    yaml_string = generate_yaml(parsed_requirements)
    validation_result = validate_yaml(yaml_string)
    
    return jsonify({
        "parsed_requirements": parsed_requirements,
        "yaml": yaml_string,
        "validation": validation_result
    })

@app.route('/api/refine-yaml', methods=['POST'])
def refine_yaml_endpoint():
    user_text = request.json.get('text', '')
    current_yaml = request.json.get('current_yaml', '')
    
    # Parse the current YAML
    current_config = yaml.safe_load(current_yaml) if current_yaml else {}
    
    # Process the refinement request
    parsed_refinement = parse_refinement_intent(user_text, current_config)
    updated_config = apply_refinement(current_config, parsed_refinement)
    
    # Convert back to YAML and validate
    updated_yaml = yaml.dump(updated_config, default_flow_style=False)
    validation_result = validate_yaml(updated_yaml)
    
    return jsonify({
        "yaml": updated_yaml,
        "validation": validation_result
    })

if __name__ == '__main__':
    app.run(debug=True)