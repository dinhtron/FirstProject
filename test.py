import pandas as pd
from sklearn.utils import resample
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup
from torch.utils.data import DataLoader, TensorDataset, RandomSampler, SequentialSampler
import torch
import torch.optim as optim
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
# Original and additional data

additional_data_address = {
    'text': [
        'Địa chỉ trường học là gì?',
        'Địa chỉ',
        'Vị trí',
        'Bạn biết địa chỉ của trường học không?',
        'Đâu là địa chỉ của trường học.',
        'Địa chỉ trường',
        'Vị trí trường',
        'Địa điểm của trường',
        'Địa chỉ',
        'Địa chỉ',
    ],
    'label': ['địa_chỉ','địa_chỉ', 'địa_chỉ', 'địa_chỉ', 'địa_chỉ', 'địa_chỉ', 'địa_chỉ','địa_chỉ', 'địa_chỉ', 'địa_chỉ' ]
}

additional_data = {
    'text': [
        'Học phí của trường này là bao nhiêu?',
        'Học phí',
        'Tôi quan tâm đến học phí của trường này',
        'Học phí như thế nào',
        'Tôi muốn biết về học phí',
        'Có phải là học phí của trường này thấp không?',
        'Học phí',
        'Học phí',
        'Học phí',
        'Học phí',
    ],
    'label': ['học_phi', 'học_phi', 'học_phi', 'học_phi', 'học_phi', 'học_phi','học_phi', 'học_phi', 'học_phi', 'học_phi']
}

additional_data_greeting = {
    'text': [
        'Xin chào',
        'Chào bạn',
        'Hi',
        'Hello',
        'Chào buổi sáng',
        'Chào buổi tối',
        'Chào bạn',
        'Chào',
        'Chào',
        'Chào',
    ],
    'label': ['chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi', 'chào_hỏi']
}
additional_data_sukien = {
    'text': [
        'Hoạt động',
        'Hoạt động',
        'Sự kiện',
        'Sự kiện',
        'Có những sự kiện nào',
        'Hoạt động đang điễn ra',
        'Có những hoạt động nào',
        'Hoạt động',
        'Sự kiện',
        'Sự kiện',
    ],
    'label': ['su_kien','su_kien', 'su_kien', 'su_kien', 'su_kien','su_kien', 'su_kien', 'su_kien','su_kien', 'su_kien']
}
tuyen_sinh = {
    'text': [
        'Thông tin về tuyển sinh trường này là gì?',
        'Tuyển sinh',
        'Quy trình tuyển sinh',
        'Bạn có biết thông tin về tuyển sinh của trường này không?',
        'Thông tin tuyển sinh của trường này là gì?',
        'Quy trình tuyển sinh',
        'Tuyển sinh',
        'Tuyển sinh',
        'Tuyển sinh',
        'Tuyển sinh',
    ],
    'label': ['tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh', 'tuyển_sinh']
}
nganh = {
    'text': [
        'Bạn quan tâm đến ngành nào?',
        'Ngành học',
        'Ngành học phổ biến',
        'Bạn có biết thông tin về các ngành học không?',
        'Thông tin về ngành học là gì?',
        'Ngành học ưa thích của bạn là gì?',
        'Bạn có biết thông tin về ngành mà bạn quan tâm không?',
        'Bạn muốn học ngành nào?',
        'Tôi muốn biết về ngành học',
        'Bạn muốn học ngành gì?',
    ],
    'label': ['nganh', 'nganh', 'nganh', 'nganh', 'nganh', 'nganh', 'nganh', 'nganh', 'nganh', 'nganh']
}

# Combine all data
lien_he = {
    'text': [
        'Liên hệ trường',
        'Thông tin liên hệ',
        'Email của trường là gì?',
        'Số điện thoại của trường?',
        'Làm sao để liên lạc với trường?',
        'Làm sao để liên hệ',
        'Liên hệ',
        'Liên hệ',
        'Liên lạc',
        'Cho tôi thông tin liên hệ',
    ],
    'label': ['liên_hệ', 'liên_hệ', 'liên_hệ',
              'liên_hệ', 'liên_hệ','liên_hệ', 'liên_hệ', 'liên_hệ', 'liên_hệ', 'liên_hệ']
}

tin_tuc = {
    'text': [
        'Có tin tức mới không?',
        'Tin tức ',
        'Cập nhật tin tức',
        'Tin tức trường học',
        'Tin tức mới nhất',
        'Tin tức',
         'Tin tức',
         'Tin tức',
         'Tin tức',
         'Tin tức',
    ],
    'label': ['tin_tức', 'tin_tức', 'tin_tức', 'tin_tức', 'tin_tức',
              'tin_tức', 'tin_tức', 'tin_tức', 'tin_tức', 'tin_tức']
}

dao_tao = {
    'text': [
        'Chương trình đào tạo',
        'Đào tạo',
        'Đào tạo',
        'Thông tin về đào tạo',
        'Đào tạo',
    ],
    'label': ['đào_tạo', 'đào_tạo', 'đào_tạo', 'đào_tạo', 'đào_tạo']
}

nghien_cuu = {
    'text': [
        'Nghiên cứu khoa học',
        'Dự án nghiên cứu',
        'Thông tin về nghiên cứu',
        'Các bài báo khoa học',
        'Nghiên cứu',
        'Khoa học',
        'Nguyên cứu',
    ],
    'label': ['nghiên_cứu', 'nghiên_cứu', 'nghiên_cứu', 'nghiên_cứu', 'nghiên_cứu',
              'nghiên_cứu', 'nghiên_cứu']
}

# Combine all data
df = pd.concat([pd.DataFrame(additional_data_address), pd.DataFrame(additional_data), pd.DataFrame(additional_data_greeting),
                pd.DataFrame(additional_data_sukien), pd.DataFrame(tuyen_sinh), pd.DataFrame(nganh),
                pd.DataFrame(lien_he), pd.DataFrame(tin_tuc), pd.DataFrame(dao_tao), pd.DataFrame(nghien_cuu)],
               ignore_index=True)

# Encode labels
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

# Balancing the dataset
df_balanced = pd.DataFrame()
for label in df['label'].unique():
    label_df = df[df['label'] == label]
    if len(label_df) < 20:
        label_df = resample(label_df, replace=True, n_samples=20, random_state=42)
    df_balanced = pd.concat([df_balanced, label_df])

# Split the dataset
train_df, test_df = train_test_split(df_balanced, test_size=0.2, random_state=42, stratify=df_balanced['label'])

# Initialize the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def encode_data(texts, labels, max_length=128):
    input_ids = []
    attention_masks = []
    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    return {
        'input_ids': torch.cat(input_ids, dim=0),
        'attention_mask': torch.cat(attention_masks, dim=0),
        'labels': torch.tensor(labels)
    }

train_data = encode_data(train_df.text.values, train_df.label.values)
test_data = encode_data(test_df.text.values, test_df.label.values)

# Load the model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(df['label'].unique()))

# Set up optimizer and scheduler
optimizer = optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
epochs = 6  # Tăng số epochs lên 6
batch_size = 8

# Create DataLoader for training and testing
train_dataset = TensorDataset(train_data['input_ids'], train_data['attention_mask'], train_data['labels'])
train_dataloader = DataLoader(train_dataset, sampler=RandomSampler(train_dataset), batch_size=batch_size)

test_dataset = TensorDataset(test_data['input_ids'], test_data['attention_mask'], test_data['labels'])
test_dataloader = DataLoader(test_dataset, sampler=SequentialSampler(test_dataset), batch_size=batch_size)

total_steps = len(train_dataloader) * epochs
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def train_model(model, train_dataloader, test_dataloader, optimizer, scheduler, epochs=6):
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        total_correct = 0
        total_samples = 0

        for step, batch in enumerate(train_dataloader):
            batch = tuple(t.to(device) for t in batch)
            input_ids, attention_mask, labels = batch

            model.zero_grad()

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()
            scheduler.step()

            # Calculate accuracy
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)
            total_correct += (preds == labels).sum().item()
            total_samples += labels.size(0)

        avg_train_loss = total_loss / len(train_dataloader)
        train_accuracy = total_correct / total_samples
        print(f"Epoch {epoch+1}, Training Loss: {avg_train_loss:.4f}, Training Accuracy: {train_accuracy:.4f}")

        # Validation
        model.eval()
        eval_loss = 0
        total_correct = 0
        total_samples = 0

        with torch.no_grad():
            for batch in test_dataloader:
                batch = tuple(t.to(device) for t in batch)
                input_ids, attention_mask, labels = batch

                outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                eval_loss += loss.item()

                logits = outputs.logits
                preds = torch.argmax(logits, dim=1)
                total_correct += (preds == labels).sum().item()
                total_samples += labels.size(0)

        avg_eval_loss = eval_loss / len(test_dataloader)
        eval_accuracy = total_correct / total_samples
        print(f"Epoch {epoch+1}, Validation Loss: {avg_eval_loss:.4f}, Validation Accuracy: {eval_accuracy:.4f}")

train_model(model, train_dataloader, test_dataloader, optimizer, scheduler, epochs)

def evaluate_model(model, test_dataloader):
    model.eval()
    predictions, true_labels = [], []

    with torch.no_grad():
        for batch in test_dataloader:
            batch = tuple(t.to(device) for t in batch)
            input_ids, attention_mask, labels = batch

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1).cpu().numpy()

            predictions.extend(preds)
            true_labels.extend(labels.cpu().numpy())

    target_names = label_encoder.inverse_transform([i for i in range(len(df['label'].unique()))])

    accuracy = accuracy_score(true_labels, predictions)
    print(f"Accuracy: {accuracy:.4f}")

    print(classification_report(true_labels, predictions, target_names=target_names))

evaluate_model(model, test_dataloader)

# Save the model
model.save_pretrained("/content/drive/MyDrive/Bert_modun/bert_model_01")


