export function StreamCanvas({ imageBase64 }) {
  return (
    <div className="panel">
      <h2>Processed Frame</h2>
      {imageBase64 ? (
        <img
          className="stream-image"
          src={`data:image/jpeg;base64,${imageBase64}`}
          alt="Processed video frame"
        />
      ) : (
        <div className="placeholder">Waiting for processed frame...</div>
      )}
    </div>
  );
}
