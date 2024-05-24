let recognition;
let soundEnabled = false;
let soundEnabled1 = false;
let soundEnabled2 = false;
function toggleToolbarVisibility() {
var toolbar = document.getElementById("toolbar");
toolbar.classList.toggle("hidden"); // Thêm hoặc loại bỏ class "hidden" để ẩn hoặc hiện thanh công cụ
}
function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() !== "") {
        appendMessage("user", userInput);
        document.getElementById("user-input").value = "";
        fetchResponse(userInput);
    }
}

function startRecording() {
    recognition = new webkitSpeechRecognition();
    recognition.lang = 'vi-VN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        let userVoiceInput = event.results[0][0].transcript;
        appendMessage("user", userVoiceInput);
        fetchResponse(userVoiceInput);
    };

    recognition.start();
}


// Gọi hàm displaySuggestedQuestions() với thông điệp "1. Học phí\n2. Lịch học"


// function appendMessage(sender, message) {
//     let chatMessages = document.getElementById("chat-messages");
//     let messageElement = document.createElement("div");
//     messageElement.classList.add("message", sender);
//     messageElement.innerText = message;
//     chatMessages.appendChild(messageElement);
//     chatMessages.scrollTop = chatMessages.scrollHeight;
// }
function icondMessage() {
    let chatMessages = document.getElementById("chat-messages");
    let messageElement = document.createElement("div");
    messageElement.classList.add("message", "bot");
    messageElement.innerHTML = `
    <i class="fas fa-robot" style="font-size: 15px;"></i>

    `;
    messageElement.style.borderRadius = "40px";
    messageElement.style.backgroundColor="rgb(214, 201, 225)"
    chatMessages.appendChild(messageElement);
}



function appendMessage(sender, message,overlay,data) {
    
    let chatMessages = document.getElementById("chat-messages");
    let messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);

    if (Array.isArray(message)) {
        messageElement.style.backgroundColor = "#fff";

        let maxWidth = 0;
        message.forEach(item => {
            let tempButton = document.createElement("button");
            tempButton.textContent = item;
            document.body.appendChild(tempButton);
            document.body.removeChild(tempButton);
        });
        
        messageElement.style.display = "flex";
        messageElement.style.boxShadow="0 0 0px rgba(0, 0, 0, 0)"
        // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

        message.forEach(item => {
            let button = document.createElement("button");
            button.textContent = item;
            button.style.padding = "30px 50px";
            button.style.backgroundColor = "rgb(214, 201, 225)";

            // button.addEventListener("click", function() {
            //     appendMessage("user", this.textContent);
            //     fetchResponse(this.textContent);
            // });
            button.addEventListener("click", function() {
                if (overlay === "phan_hoi"){
                    phan_hoi(item);
                } else{
                    showOverlay(item,data);
                }
                
            });
            messageElement.appendChild(button);
        });

    } else {
        messageElement.textContent = message;
    }
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    if (sender=="bot") {
        if (lastBotMessage !== null) {
            lastBotMessage.remove();
        }
        
    }
    // Chỉ thêm nút "Mở màn hình phụ" nếu sender là "bot"
    if (overlay === "true" && sender=="bot") {
        let openOverlayButton = document.createElement("button");
        openOverlayButton.textContent = "xem thêm";
        openOverlayButton.classList.add("overlay-button");
        openOverlayButton.addEventListener("click", function() {
            showOverlay2(data);
        });
        let lineBreak = document.createElement("br");
        messageElement.appendChild(lineBreak);

        // Thêm nút button và phần tử xuống dòng vào messageElement
        messageElement.appendChild(openOverlayButton);
    }
    checkAndAddMessage();
}
let lastBotMessage = null;

        // Hàm kiểm tra và thêm thẻ message mới nếu điều kiện đúng
function checkAndAddMessage() {
            const chatMessages = document.getElementById('chat-messages');
            const messages = chatMessages.getElementsByClassName('message');
            
            if (messages.length > 0) {
                const lastMessage = messages[messages.length - 1];
                
                if (lastMessage.classList.contains('user')) {
                    const newMessage = document.createElement('div');
                    newMessage.className = 'message bot';
                    newMessage.innerHTML = '<div class="ellipsis"><div></div><div></div><div></div></div>';
                    newMessage.style.marginLeft = '5px';
                    // Xóa tin nhắn bot cuối cùng nếu có
                    if (lastBotMessage !== null) {
                        lastBotMessage.remove();
                    }
                    
                    // Thêm tin nhắn mới từ bot và lưu lại
                    chatMessages.appendChild(newMessage);
                    lastBotMessage = newMessage;
                }
            }
        }
function phan_hoi(item) {
    var itemParagraph = document.getElementById("itemParagraph");
    itemParagraph.textContent = item;
    document.getElementById("name").value = item; // Đặt giá trị cho input name
    document.getElementById("popup-overlay").classList.add("active");
}

function showOverlay2(data) {
    // Create the overlay element
    var overlay = document.createElement('div');
    overlay.id = 'overlay';
    overlay.style.zIndex = '9999';
    overlay.style.display = 'flex';

    // Create the content div
    var contentDiv = document.createElement('div');
    contentDiv.id = 'overlay-content';

    // Add content to the content div
    for (let key in data) {
        // Kiểm tra nếu key là một thuộc tính của đối tượng data và không phải là "id" hoặc "id_user"
        if (data.hasOwnProperty(key) && key !== 'id' && key !== 'id_user') {
            // Thêm cặp key-value vào chuỗi output
            contentDiv.innerHTML += `<p>${key}: ${data[key]}</p>`;
        }
    }


    // Thêm nút đóng vào contentDiv
    contentDiv.innerHTML =`<p>Điểm thi của bạn là :</p> `+contentDiv.innerHTML+`<button onclick="hideOverlay()">Đóng</button>`;

    // Append the content div to the overlay
    overlay.appendChild(contentDiv);

    // Append the overlay to the body
    document.body.appendChild(overlay);
}

function showOverlay(item,data_hoatdong) {
    console.log(data_hoatdong); 
    // Create the overlay element
    // let hoatdongStr = data_hoatdong.map(hoatdong => hoatdong.name);
    let hoatdongStr = (data_hoatdong.find(hoatdong => hoatdong.name === item) || {}).information;
    var overlay = document.createElement('div');
    overlay.id = 'overlay';
    overlay.style.zIndex = '9999';
    overlay.style.display = 'flex';
    // Create the content div
    var contentDiv = document.createElement('div');
    contentDiv.id = 'overlay-content';
    // Add content to the content div
    contentDiv.innerHTML = `
        <h2>Tên sự kiên:${item}</h2>
        <p>Nội dung:  ${hoatdongStr}</p>
        <button onclick="hideOverlay()">Đóng</button>
    `;

    // Append the content div to the overlay
    overlay.appendChild(contentDiv);

    // Append the overlay to the body
    document.body.appendChild(overlay);
}

function hideOverlay() {
    var overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.parentNode.removeChild(overlay);
    }
}

function speak(text) {
    if (soundEnabled) {
        let synth = window.speechSynthesis;
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'vi-VN';
        synth.speak(utterance);
    }
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    let soundStatusElement = document.getElementById("sound-status");
    soundStatusElement.innerHTML = soundEnabled ? '<i class="fas fa-volume-up"></i>' : '<i class="fas fa-volume-mute"></i>';
}

let currentMode = 'rasa'; // Initial mode is 'rasa'

function updet() {
    let nextMode;
    let soundStatusElement = document.getElementById("status");
    let url;
    let url1;

    // Determine the next mode
    switch (currentMode) {
        case 'rasa':
            nextMode = 'gpt';
            url = "/update_toggle";
            soundStatusElement.innerHTML = nextMode.charAt(0).toUpperCase() + nextMode.slice(1);
            currentMode = nextMode;
        
            // Send the update to the server
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ toggle: nextMode }));
            break;
        case 'gpt':
            nextMode = 'bert';
            url = "/update_toggle_bert";
            soundStatusElement.innerHTML = nextMode.charAt(0).toUpperCase() + nextMode.slice(1);
            currentMode = nextMode;
        
            // Send the update to the server
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ toggle: nextMode }));
            break;
        case 'bert':
            nextMode = 'rasa';
            url = "/update_toggle_bert";
            url1 = "/update_toggle";
            soundStatusElement.innerHTML = nextMode.charAt(0).toUpperCase() + nextMode.slice(1);
            currentMode = nextMode;
        
            // Send the update to the server
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ toggle: nextMode }));
            
            soundStatusElement.innerHTML = nextMode.charAt(0).toUpperCase() + nextMode.slice(1);
            currentMode = nextMode;
        
            // Send the update to the server
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url1, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ toggle: nextMode }));
            break;
    }

    // Update the mode status
 
}




function checkScroll() {
    var element = document.getElementById("chat-messages");
    if (element.scrollHeight > element.clientHeight) {
        element.style.overflowY = "scroll";
    } else {
        element.style.overflowY = "hidden";
    }
}
