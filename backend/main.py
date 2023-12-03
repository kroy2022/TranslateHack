from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer
import requests
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRIVATE_KEY='f06a64ca-b272-4589-96f5-1ed1fd0ea09b'

class User(BaseModel):
    username: str

@app.post('/englishToSpanish')
def englishToSpanish(input_text_english):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reached engToSpan function")

    # Load pre-trained model and tokenizer
    model_name = "Helsinki-NLP/opus-mt-en-es"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # Encode input text
    input_ids = tokenizer.encode(input_text_english, return_tensors="pt")

    # Generate translation
    output_ids = model.generate(input_ids)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    logging.debug("Translated Text in Python: %s", output_text)
    return output_text

@app.post('/spanishToEnglish')
def spanishToEnglish(input_text):
    # Load pre-trained model and tokenizer for Spanish-to-English translation
    model_name = "Helsinki-NLP/opus-mt-es-en"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # Encode input text in Spanish
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate translation to English
    output_ids = model.generate(input_ids)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return output_text

@app.post('/authenticate')
async def authenticate(user: User):
    response = requests.put('https://api.chatengine.io/users/',
        data = {
            "username": user.username,
            "secret": user.username,
            "first_name": user.username,
        },
        headers={"Private-Key": PRIVATE_KEY}
    )
    return response.json()

@app.post("/translateMessage")
async def translate(message: dict):
    """""
    text_Eng = message.get("message", " ")

    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    #translate english to spanish
    tokenizer.src_lang = "en_XX"
    encoded_Eng = tokenizer(text_Eng, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded_Eng,
        forced_bos_token_id = tokenizer.lang_code_to_id["es_XX"]
    )
    translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return {"translated_message": translated}
    """
    incoming_message = message.get("message", " ")
    translated_message = incoming_message + " Added "
    return {"translated_message": translated_message}
#projectID: 7c2c3ea1-3c0e-4a99-a456-bea13d6a618b


