import { useEffect, useRef, useState } from "react";
import { INGEST_WS_URL } from "../config";

export function useCameraStream() {
  const videoRef = useRef(null);
  const [status, setStatus] = useState("idle");
  const [imageBase64, setImageBase64] = useState("");
  const [roi, setRoi] = useState(null);

  useEffect(() => {
    let mediaStream;
    let socket;
    let intervalId;
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    async function start() {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }

        socket = new WebSocket(INGEST_WS_URL);
        socket.onopen = () => {
          setStatus("connected");
          intervalId = window.setInterval(() => {
            const video = videoRef.current;
            if (!video || video.videoWidth === 0 || socket.readyState !== WebSocket.OPEN) {
              return;
            }

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL("image/jpeg", 0.7);
            socket.send(
              JSON.stringify({
                frame_id: crypto.randomUUID(),
                source_id: "default",
                image_base64: dataUrl,
              }),
            );
          }, 400);
        };
        socket.onmessage = (event) => {
          const message = JSON.parse(event.data);
          if (message.type === "processed_frame") {
            setImageBase64(message.payload.image_base64);
            setRoi(
              message.payload.roi
                ? {
                    session_id: message.payload.session_id,
                    frame_id: message.payload.frame_id,
                    source_id: message.payload.source_id,
                    detected_at: message.payload.detected_at,
                    ...message.payload.roi,
                  }
                : null,
            );
          }
          if (message.type === "error") {
            setStatus("error");
          }
        };
        socket.onerror = () => setStatus("error");
        socket.onclose = () => setStatus("closed");
      } catch (error) {
        console.error(error);
        setStatus("error");
      }
    }

    start();

    return () => {
      if (intervalId) {
        window.clearInterval(intervalId);
      }
      if (socket) {
        socket.close();
      }
      if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return { videoRef, status, imageBase64, roi };
}
