import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load mô hình đã huấn luyện
model = BertForSequenceClassification.from_pretrained("bert_model")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Đoạn văn bản bạn muốn thử nghiệm
text_to_test = "địa chỉ ở đâu"

# Mã hóa đoạn văn bản
encoded_text = tokenizer.encode_plus(
    text_to_test,
    add_special_tokens=True,
    max_length=128,
    padding='max_length',
    truncation=True,
    return_attention_mask=True,
    return_tensors='pt',
)

# Lấy dự đoán từ mô hình
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()

# Hiển thị dự đoán
if predicted_label == 1:
    print("Đoạn văn bản được dự đoán là về 'học_phi'")
elif predicted_label == 2:
    print("Đoạn văn bản được dự đoán là về 'địa_chỉ'")
else:
    print("Đoạn văn bản được dự đoán không liên quan đến 'học_phi' hoặc 'địa_chỉ'")
