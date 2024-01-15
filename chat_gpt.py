import random
import json
from openai import OpenAI
import time

TEST_OPENAI_API_KEY = API_KEY


def get_llm_response(user_prompt, system_prompt):
    client = OpenAI(
        api_key=TEST_OPENAI_API_KEY,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return completion.choices[0].message.content


def generate_movie_script(prompt, universe):
    dialogue =[]
    for location in universe['locations']:
        characters_in_scene = []

        for character, about in universe["characters"].items():
                characters_in_scene.append(f'{character} - {about}')
        
        characters_in_scene = random.sample(characters_in_scene, k=random.randint(1, len(universe["characters"])))
        main_character = random.choice(characters_in_scene)
        characters_in_scene.remove(main_character)

        user_pompt =f'''You are {main_character}. 
You are in a location: {location} - {universe.get("locations", {}).get(location)}. 
Your task is to engage in a dialogue with the characters in the location or to think about something if you are alone:{characters_in_scene if characters_in_scene else 'you are alone'} (Figure out what they're doing).
''' + "(Don't use actions in the dialogue, the characters should only talk)"
        system_prompt = f'You are doing: {prompt}. Use only these emotions: {universe["emotions"]}' +'Come up with a dialogue between them using the JSON format: {"location": "", "characters": [(The names of all the characters who speak)], "dialogue": [{"speaker": "", "text": "", "emotion": ""}]} (after the last element, do not put ",")'
        str_in_dict = get_llm_response(user_pompt, system_prompt)
        str_in_dict = json.loads(str_in_dict)
        dialogue.append(str_in_dict)
        time.sleep(6)
        
    return dialogue
    
    


if __name__ == "__main__":
    prompt = 'The characters are late for the train' #"Hanging around looking for something to do"

    universe = {
        "characters": {
            "Alice": "7 years old girl, very curious",
            "Jack": "Alice's brother, 10 years old, likes to play with his friends",
            "Bob": "Alice's father, a programmer",
            "Mary": "Alice's mother, a teacher",
        },
        "locations": {
            "reception": "a big room in Alice's house with a big table, TV and a fireplace",
            "kitchen": "a cosy kitchen in Alice's house",
            "hall": "a long hall in Alice's house",
            "park": "a park near Alice's house",
        },
        "emotions": ["happy", "sad", "angry", "surprised", "scared"],
    }

    generated_script = generate_movie_script(prompt, universe)
    
    print(json.dumps(generated_script, indent=4))
    

    
    
    