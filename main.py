import json
from jsonschema import validate, ValidationError


# Step 1: Define the JSON schema
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "experience_level": {
            "type": "string",
            "enum": ["Beginner", "Intermediate", "Advanced"]
        },
        "recommended_role": {"type": "string"}
    },
    "required": [
        "name",
        "skills",
        "experience_level",
        "recommended_role"
    ],
    "additionalProperties": False
}


# Step 2: Generate sample output
def generate_output(attempt):
    # First attempt deliberately returns invalid data
    if attempt == 1:
        return {
            "name": "Ramya",
            "skills": ["Python", "SQL"],
            "experience_level": "Expert",
            "recommended_role": "AI/ML Intern"
        }

    # Second attempt returns valid data
    return {
        "name": "Ramya",
        "skills": ["Python", "Machine Learning", "SQL"],
        "experience_level": "Beginner",
        "recommended_role": "AI/ML Intern"
    }


# Step 3: Validate output and retry if needed
def get_valid_output(max_retries=3):

    for attempt in range(1, max_retries + 1):

        try:
            print(f"Attempt {attempt}")

            output = generate_output(attempt)

            # Convert dictionary to JSON
            json_text = json.dumps(output)

            # Parse JSON
            parsed_output = json.loads(json_text)

            # Validate against schema
            validate(
                instance=parsed_output,
                schema=OUTPUT_SCHEMA
            )

            print("Validation successful!")
            return parsed_output

        except (json.JSONDecodeError, ValidationError) as error:

            print("Invalid output:", error.message)

            if attempt == max_retries:
                raise ValueError(
                    "Failed to generate valid JSON after retries."
                ) from error

            print("Retrying...\n")

    raise ValueError("No valid output generated.")


# Step 4: Run the program
if __name__ == "__main__":

    try:
        result = get_valid_output()

        print("\nFinal Valid JSON Output:")
        print(json.dumps(result, indent=4))

    except ValueError as error:
        print("Error:", error)