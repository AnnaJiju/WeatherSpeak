// Simple voice recording weather agent
document.addEventListener("DOMContentLoaded", () => {
    console.log('Voice Weather Agent initialized');
    
    const startBtn = document.getElementById("startBtn");
    if (startBtn) {
        startBtn.addEventListener("click", recordAudio);
        console.log('Button listener attached');
    }
});

async function recordAudio() {
    const status = document.getElementById("status");
    const startBtn = document.getElementById("startBtn");
    
    // Disable button during recording
    if (startBtn) {
        startBtn.disabled = true;
        startBtn.innerText = "Recording...";
    }
    
    status.innerText = "🎤 Requesting microphone access...";

    try {
        // Check if MediaRecorder is supported
        if (typeof MediaRecorder === "undefined") {
            throw new Error("MediaRecorder API is not supported in this browser.");
        }

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
            console.log('Audio chunk received:', event.data.size, 'bytes');
        };

        mediaRecorder.onstop = async () => {
            console.log('Recording stopped, processing audio...');
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            console.log('Audio blob created:', audioBlob.size, 'bytes');
            
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.wav");

            status.innerText = "📤 Uploading audio to server...";

            try {
                const response = await fetch("http://127.0.0.1:8000/process-audio", {
                    method: "POST",
                    body: formData,
                });

                console.log('Response status:', response.status);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Server error:', errorText);
                    throw new Error(`Failed to process audio: ${response.status} - ${errorText}`);
                }

                // Get the response as JSON
                const responseData = await response.json();
                console.log('Server response:', responseData);
                
                let audioPath = responseData.audio_path;
                console.log('Audio path:', audioPath);
                
                // Construct full URL
                let audioUrl;
                if (audioPath.startsWith('http')) {
                    audioUrl = audioPath;
                } else {
                    // Remove leading slash if present
                    audioPath = audioPath.startsWith('/') ? audioPath.slice(1) : audioPath;
                    audioUrl = `http://127.0.0.1:8000/${audioPath}`;
                }
                
                console.log('Playing audio from:', audioUrl);
                status.innerText = "🔊 Playing weather details...";

                const audio = new Audio(audioUrl);
                
                // Add error handler for audio playback
                audio.onerror = (e) => {
                    console.error('Audio playback error:', e);
                    console.error('Failed audio URL:', audioUrl);
                    status.innerText = `❌ Failed to play audio. Check console for details.`;
                    if (startBtn) {
                        startBtn.disabled = false;
                        startBtn.innerText = "Try Again";
                    }
                };
                
                audio.onloadeddata = () => {
                    console.log('Audio loaded successfully, duration:', audio.duration);
                };
                
                audio.onended = () => {
                    console.log('Audio playback finished');
                    status.innerText = "✅ Weather details played successfully!";
                    if (startBtn) {
                        startBtn.disabled = false;
                        startBtn.innerText = "Ask Again";
                    }
                };
                
                // Play the audio
                await audio.play();
                
            } catch (fetchError) {
                console.error('Fetch error:', fetchError);
                status.innerText = `❌ Server error: ${fetchError.message}`;
                if (startBtn) {
                    startBtn.disabled = false;
                    startBtn.innerText = "Try Again";
                }
            }
            
            // Stop all tracks to release microphone
            stream.getTracks().forEach(track => track.stop());
        };

        status.innerText = "🎤 Recording... (5 seconds)";
        mediaRecorder.start();
        console.log('Recording started');

        // Record for 5 seconds
        setTimeout(() => {
            console.log('Stopping recording...');
            mediaRecorder.stop();
            status.innerText = "⏳ Processing your request...";
        }, 5000);

    } catch (err) {
        console.error("Audio recording error:", err);
        status.innerText = `❌ Error: ${err.message}`;
        if (startBtn) {
            startBtn.disabled = false;
            startBtn.innerText = "Try Again";
        }
    }
}