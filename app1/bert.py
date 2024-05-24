import torch
from transformers import BertTokenizer, BertForSequenceClassification

def bert_modun(user_message):
         model = BertForSequenceClassification.from_pretrained("bert_model")
         tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

         # Đoạn văn bản bạn muốn thử nghiệm
         text_to_test = user_message 

       # Encode the text
         encoded_text = tokenizer.encode_plus(
            text_to_test,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
         )

         # Extract input_ids and attention_mask
         input_ids = encoded_text['input_ids']
         attention_mask = encoded_text['attention_mask']

         # Get predictions from the model
         with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predicted_label = torch.argmax(logits, dim=1).item()

         # Display prediction based on label
         response_map = {
               0: "Xin chào bạn, mình có thể giúp gì cho bạn hôm nay?",
               1: "Học phí của trường thay đổi tùy theo chương trình đào tạo, bạn muốn biết thêm chi tiết về chương trình nào không?",
               2: "Kí túc xá của chúng tôi rất thoải mái và tiện nghi, bạn cần biết thêm chi tiết nào không?",
               3: "Nếu bạn cần liên hệ, vui lòng cho mình biết vấn đề cụ thể để mình có thể hướng dẫn bạn đến đúng bộ phận.",
               4: "Chúng tôi có rất nhiều ngành học thú vị, bạn đang quan tâm đến ngành nào?",
               5: "Nghiên cứu là một phần quan trọng của trường, bạn muốn tìm hiểu thêm về lĩnh vực nào?",
               6: "phan_hoi",
               7: "hoat_dong",
               8: "Thư viện của chúng tôi có rất nhiều tài liệu hữu ích, bạn cần tìm thông tin gì cụ thể không?",
               9: "Tin tức mới nhất của trường luôn được cập nhật, bạn muốn biết về thông tin nào?",
               10: "Chương trình tuyển sinh của trường có rất nhiều thông tin hữu ích, bạn cần hỗ trợ gì thêm không?",
               11: "Tạm biệt bạn, chúc bạn một ngày tốt lành!",
               12: "diem_thi",
               13: "Chương trình đào tạo của chúng tôi rất đa dạng, bạn quan tâm đến khóa học nào?",
               14: "Địa chỉ của trường là 54 Nguyễn Lương Bằng, bạn có cần thêm chỉ dẫn không?"
            }


         bot_response = response_map.get(predicted_label, "xin lỗi k tìm ra kết quả")

         return bot_response