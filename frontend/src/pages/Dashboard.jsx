import { RoiPanel } from "../components/RoiPanel";
import { StatusBadge } from "../components/StatusBadge";
import { StreamCanvas } from "../components/StreamCanvas";
import { useCameraStream } from "../hooks/useCameraStream";

export function Dashboard() {
  const { videoRef, status, imageBase64, roi } = useCameraStream();

  return (
    <main className="app-shell">
      <section className="header">
        <div>
          <h1>Face Stream</h1>
          <p className="lede">Webcam frames are sent over WebSocket and returned with face ROI metadata.</p>
        </div>
        <StatusBadge label={status} state={status} />
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Webcam</h2>
          <video className="stream-image" ref={videoRef} autoPlay muted playsInline />
        </div>
        <StreamCanvas imageBase64={imageBase64} />
        <RoiPanel roi={roi} />
      </section>
    </main>
  );
}
