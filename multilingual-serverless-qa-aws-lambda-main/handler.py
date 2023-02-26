import json
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoConfig

def encode(tokenizer, text):
    """encodes the question and context with a given tokenizer"""
    encoded = tokenizer.encode_plus(text)
    return encoded["input_ids"], encoded["attention_mask"]

def decode(tokenizer, token):
    """decodes the tokens to the answer with a given tokenizer"""
    answer_tokens = tokenizer.convert_ids_to_tokens(
        token, skip_special_tokens=True)
    return tokenizer.convert_tokens_to_string(answer_tokens)
      
def serverless_pipeline(model_path='./model'):
    """Initializes the model and tokenzier and returns a predict function that ca be used as pipeline"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForMaskedLM.from_pretrained(model_path)
    def predict(question, text):
        input_ids, attention_mask = encode(tokenizer, text)
        start_scores, end_scores = model(torch.tensor(
            [input_ids]), attention_mask=torch.tensor([attention_mask]))
        ans_tokens = input_ids[torch.argmax(
            start_scores): torch.argmax(end_scores)+1]
        answer = decode(tokenizer,ans_tokens)        
        return answer
    return predict

# initializes the pipeline
machine_translation_pipeline = serverless_pipeline()

def handler(event, text):
    try:
        body = json.loads(event['body'])
        print(body)
        # uses the pipeline to predict the answer
        answer = machine_translation_pipeline(text=body['text'])
        print(answer)
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True

            },
            "body": json.dumps({'answer': answer})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }