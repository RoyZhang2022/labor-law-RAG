from transformers import AutoTokenizer, AutoModel

model_name = 'moka-ai/m3e-base'

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

tokenizer.save_pretrained('./m3e-base')
model.save_pretrained('./m3e-base')
