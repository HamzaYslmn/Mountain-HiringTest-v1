document.addEventListener('DOMContentLoaded', () => {
    const chatBody = document.getElementById('chat-body');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const microphoneBtn = document.getElementById('microphone-btn');
    const paperclipBtn = document.getElementById('paperclip-btn');
    const chatFooter = document.querySelector('.chat-footer');
    const countdownClock = document.getElementById('countdown-clock');
    const countdownTime = parseInt(document.querySelector('meta[name="countdown"]').getAttribute("content"), 10);
    const voiceToggle = document.getElementById('voice-toggle');
    const username = document.querySelector('meta[name="username"]').getAttribute("content");

    let isProcessing = false;
    let recording = false;
    let selectedFile = null;
    let mediaRecorder;
    let audioChunks = [];
    let mediaStream;
    let threadId = 'new';
    let assistant_id = document.querySelector('meta[name="assistant"]').getAttribute("content");
    let RecordTimerInterval;
    let timerStarted = false;
    let countdownInterval;
    let EndOfSession = false;

    sendBtn.addEventListener('click', () => {
        if (!isProcessing) handleSendButtonClick();
    });
    microphoneBtn.addEventListener('click', toggleRecording);
    paperclipBtn.addEventListener('click', toggleImageSelection);
    messageInput.addEventListener('keydown', handleKeyDown);

    async function handleSendButtonClick() {
        if (isProcessing) return;
        isProcessing = true;

        try {
            if (recording) {
                showTypingIndicator();
                await stopRecording();
            } else {
                const message = messageInput.value.trim();
                if (selectedFile) {
                    disableUI();
                    addMessageBubbleWithImage(URL.createObjectURL(selectedFile), message, 'user');
                    showTypingIndicator();
                    await sendImage(message);
                    selectedFile = null;
                    paperclipBtn.innerHTML = '<i class="fas fa-paperclip"></i>';
                    messageInput.value = '';
                } else if (message) {
                    disableUI();
                    addMessageBubble(message, 'user');
                    showTypingIndicator();
                    await sendMessageToChatbot(message);
                    messageInput.value = '';
                }
            }

            if (!timerStarted && countdownTime > 0) {
                timerStarted = true;
                startCountdown();
            }
        } catch (error) {
            console.error('Error in handleSendButtonClick:', error);
        } finally {
            isProcessing = false;
            enableUI();
        }
    }

    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey && !isProcessing) {
            event.preventDefault();
            handleSendButtonClick();
        }
    }

    function toggleRecording() {
        if (isProcessing) return;
        recording ? cancelRecording() : startRecording();
    }

    function toggleImageSelection() {
        if (isProcessing) return;
        selectedFile ? deselectImage() : selectImage();
    }

    async function startRecording() {
        if (isProcessing || recording) return;
        isProcessing = true;

        try {
            recording = true;
            audioChunks = [];
            updateRecordingUI(true);
            startTimer();

            // Request the default audio input device
            const devices = await navigator.mediaDevices.enumerateDevices();
            const audioDevices = devices.filter(device => device.kind === 'audioinput');
            
            // If you want to use the first available audio input device
            const defaultDeviceId = audioDevices.length > 0 ? audioDevices[0].deviceId : 'default';

            mediaStream = await navigator.mediaDevices.getUserMedia({ audio: { deviceId: defaultDeviceId } });
            mediaRecorder = new MediaRecorder(mediaStream);
            mediaRecorder.start();
            mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        } catch (error) {
            console.error('Error starting recording:', error);
            cancelRecording();
        } finally {
            isProcessing = false;
        }
    }

    async function stopRecording() {
        if (!recording) return;
        recording = false;
        updateRecordingUI(false);
        stopTimer();
        disableUI();

        return new Promise((resolve) => {
            mediaRecorder.onstop = async () => {
                stopAllMediaTracks();
                if (audioChunks.length > 0) {
                    await handleSTTRequest();
                }
                resolve();
            };
            mediaRecorder.stop();
        });
    }

    function cancelRecording() {
        if (!recording) return;
        recording = false;
        updateRecordingUI(false);
        stopTimer();
    
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
        stopAllMediaTracks();
        audioChunks = []; // Clear the audio chunks
    }

    function updateRecordingUI(isRecording) {
        microphoneBtn.innerHTML = isRecording ? '<i class="fas fa-times"></i>' : '<i class="fas fa-microphone"></i>';
        sendBtn.innerHTML = isRecording ? '<i class="fas fa-stop"></i>' : '<i class="fas fa-paper-plane"></i>';
    }

    function stopAllMediaTracks() {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            mediaStream = null;
        }
    }

    async function handleSTTRequest() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_file', audioBlob);
        formData.append('thread_id', threadId);
        formData.append('assistant_id', assistant_id);
    
        try {
            const response = await fetch('/stt/', { method: 'POST', body: formData });
    
            if (!response.ok) {
                const errorText = await response.text();  // Read the error text to diagnose
                console.error('Error response from server:', errorText);
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
    
            const data = await response.json();
            addMessageBubble(data.stt_response, 'user');
    
            if (!data.stt_response.includes('ERR')) {
                showTypingIndicator();
                await sendMessageToChatbot(data.stt_response);
            }
        } catch (error) {
            console.error('Error in handleSTTRequest:', error);
            addMessageBubble('An error occurred while processing your audio. Please try again.', 'system');
        } finally {
            enableUI();
        }
    }

    async function sendMessageToChatbot(message) {
        const formData = new FormData();
        formData.append('userinput', message);
        formData.append('thread_id', threadId);
        formData.append('assistant_id', assistant_id);
        formData.append('username', username);

        try {
            const response = await fetch('/chatbot/', { method: 'POST', body: formData });
            const data = await response.json();
            for (const responseItem of data) {
                await addMessageBubble(responseItem.assistant_response, 'reply');
                threadId = responseItem.thread_id;
            }
        } catch (error) {
            console.error('Error in sendMessageToChatbot:', error);
        } finally {
            if (EndOfSession) {
                addMessageBubble("Interview No: " + threadId, 'reply');
            }
        }
    }

    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = `<span>Typing</span>&nbsp;<span class="dot">.</span>&nbsp;<span class="dot">.</span>&nbsp;<span class="dot">.</span>`;
        chatBody.appendChild(typingIndicator);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function hideTypingIndicator() {
        document.querySelector('.typing-indicator')?.remove();
    }

    function selectImage() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/png, image/jpeg, image/jpg';
        input.onchange = event => {
            selectedFile = event.target.files[0];
            if (selectedFile) {
                alert('Photo selected: ' + selectedFile.name);
                paperclipBtn.innerHTML = '<i class="fas fa-times-circle red-circle"></i>';
            }
        };
        input.click();
    }

    function deselectImage() {
        selectedFile = null;
        paperclipBtn.innerHTML = '<i class="fas fa-paperclip"></i>';
    }

    async function sendImage(message) {
        if (!selectedFile) return;
        
        const formData = new FormData();
        formData.append('image_file', selectedFile);
        formData.append('userinput', message);
        formData.append('thread_id', threadId);
        formData.append('assistant_id', assistant_id);
        formData.append('username', username);
    
        try {
            const response = await fetch('/vision/', { method: 'POST', body: formData });
            
            if (!response.ok) {
                const errorText = await response.text(); // Read error text to diagnose
                console.error('Error response from server:', errorText);
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
    
            const data = await response.json();
            await addMessageBubble(data.VisionOutput, 'reply');
        } catch (error) {
            console.error('Error in sendImage:', error);
            addMessageBubble('An error occurred while processing your image. Please try again.', 'system');
        } finally {
            hideTypingIndicator();
        }
    }    

    function createMessageBubble(type) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', type === 'user' ? 'user-message' : 'reply-message');
        return messageBubble;
    }

    async function addMessageBubble(message, type) {
        if (type === 'reply' && voiceToggle.checked) {
            await playTTSAndAddBubble(message, type);
        } else {
            createAndAppendBubble(message, type);
        }
    }

    function createAndAppendBubble(message, type) {
        hideTypingIndicator();
        const messageBubble = createMessageBubble(type);
        const messageText = document.createElement('div');
        messageText.innerHTML = type === 'reply' ? marked.parse(message) : message;
        messageBubble.appendChild(messageText);

        const headphoneIcon = document.createElement('i');
        headphoneIcon.classList.add('fas', 'fa-headphones-alt', 'headphone-icon');
        headphoneIcon.addEventListener('click', () => playTTS(message));
        messageBubble.appendChild(headphoneIcon);

        chatBody.appendChild(messageBubble);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function playTTSAndAddBubble(message, type) {
        try {
            const audioBuffer = await fetchTTSAudio(message);
            createAndAppendBubble(message, type);
            await playAudioBuffer(audioBuffer);
        } catch (error) {
            console.error('Error in playTTSAndAddBubble:', error);
        }
    }

    function addMessageBubbleWithImage(imgSrc, message, type) {
        const messageBubble = createMessageBubble(type);
        const image = document.createElement('img');
        image.src = imgSrc;
        image.alt = "Selected Photo";
        image.classList.add('selected-photo');
        messageBubble.appendChild(image);

        if (message) {
            const messageText = document.createElement('div');
            messageText.textContent = message;
            messageBubble.appendChild(messageText);
        }

        const headphoneIcon = document.createElement('i');
        headphoneIcon.classList.add('fas', 'fa-headphones-alt', 'headphone-icon');
        headphoneIcon.addEventListener('click', () => playTTS(message));
        messageBubble.appendChild(headphoneIcon);

        chatBody.appendChild(messageBubble);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function playTTS(message) {
        try {
            const audioBuffer = await fetchTTSAudio(message);
            await playAudioBuffer(audioBuffer);
        } catch (error) {
            console.error('Error in playTTS:', error);
        }
    }

    async function fetchTTSAudio(message) {
        const response = await fetch('/tts/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_input: message }),
        });
    
        if (!response.ok) {
            const errorText = await response.text(); // Read the error text to diagnose
            console.error('Error response from server:', errorText);
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
    
        const audioData = await response.arrayBuffer();
    
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        try {
            const audioBuffer = await audioContext.decodeAudioData(audioData);
            return audioBuffer;
        } catch (e) {
            console.error('Error decoding audio data:', e);
            throw e;
        }
    }    

    function playAudioBuffer(audioBuffer) {
        return new Promise((resolve, reject) => {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
    
            source.onended = resolve;
            source.onerror = reject;
    
            source.start();
        });
    }

    function startTimer() {
        const timerElement = document.createElement('div');
        timerElement.id = 'recording-timer';
        timerElement.textContent = '00:00';
        chatFooter.appendChild(timerElement);

        let seconds = 0;
        RecordTimerInterval = setInterval(() => {
            seconds++;
            timerElement.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(RecordTimerInterval);
        document.getElementById('recording-timer')?.remove();
    }

    function startCountdown() {
        let remainingTime = countdownTime;
        countdownClock.style.display = 'block';

        countdownInterval = setInterval(() => {
            remainingTime--;
            countdownClock.textContent = `${String(Math.floor(remainingTime / 60)).padStart(2, '0')}:${String(remainingTime % 60).padStart(2, '0')}`;

            if (remainingTime <= 0) {
                clearInterval(countdownInterval);
                disableUI();
                EndOfSession = true;
                sendMessageToChatbot("I have completed my time, now give me my scoring result.");
            }
        }, 1000);
    }

    function disableUI() {
        sendBtn.disabled = true;
        microphoneBtn.disabled = true;
        paperclipBtn.disabled = true;
        messageInput.disabled = true;
    }

    function enableUI() {
        sendBtn.disabled = false;
        microphoneBtn.disabled = false;
        paperclipBtn.disabled = false;
        messageInput.disabled = false;
    }
});
