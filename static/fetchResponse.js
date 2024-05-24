function fetchResponse(input) {
    fetch("/webhook", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: input
        })
    })
    .then(response => response.json())
    .then(data => {
        let botResponse = data.response;
        let data_hoatdong = data.dulieu;
        overlay = "";
        icondMessage();
        if (botResponse === "hoat_dong") {
            appendMessage("bot", "Dưới đây là các hoạt động đang diễn ra",overlay);
            let hoatdongStr = data_hoatdong.map(hoatdong => hoatdong.name);
            appendMessage("bot", hoatdongStr,overlay,data_hoatdong);
        }
        else if (botResponse === "diem_thi") {
            overlay = "true";
            appendMessage("bot", "Ấn vào để xem điểm thi: ", overlay, data_hoatdong);
        } 
        else if (botResponse === "phan_hoi") {
            overlay="phan_hoi";
            appendMessage("bot", "Vui lòng chọn loại thông tin :");
            appendMessage("bot",["Cơ sở vật chất", "Yêu cầu phúc khảo","Khác"], overlay);
        } 
          else {
            // Nếu không, chỉ gửi phản hồi đơn lẻ
            appendMessage("bot", botResponse,overlay);
            speak(botResponse);
        }
    })
    .catch(error => console.error('Error:', error));
}
