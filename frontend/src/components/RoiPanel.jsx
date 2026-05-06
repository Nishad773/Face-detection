export function RoiPanel({ roi }) {
  return (
    <div className="panel">
      <h2>ROI Metadata</h2>
      {roi ? (
        <dl className="roi-grid">
          <div><dt>Session</dt><dd>{roi.session_id}</dd></div>
          <div><dt>Frame</dt><dd>{roi.frame_id}</dd></div>
          <div><dt>X</dt><dd>{roi.x}</dd></div>
          <div><dt>Y</dt><dd>{roi.y}</dd></div>
          <div><dt>Width</dt><dd>{roi.width}</dd></div>
          <div><dt>Height</dt><dd>{roi.height}</dd></div>
          <div><dt>Detected</dt><dd>{roi.detected_at ?? "n/a"}</dd></div>
        </dl>
      ) : (
        <div className="placeholder">No face detected yet.</div>
      )}
    </div>
  );
}
