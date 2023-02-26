import os
os.environ["HF_ENDPOINT"] = "https://huggingface.co"

from transformers import AutoTokenizer, AutoModelForMaskedLM


def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = AutoModelForMaskedLM.from_pretrained(model,use_cdn=True)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)
  
def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)
  
get_model('deepset/xlm-roberta-base')
get_tokenizer('deepset/xlm-roberta-base')
# get_model('mrm8488/bert-multi-cased-finetuned-xquadv1')
# get_tokenizer('mrm8488/bert-multi-cased-finetuned-xquadv1')