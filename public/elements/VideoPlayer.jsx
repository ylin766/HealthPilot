import React from "react";

export default function VideoPlayer() {
  const containerStyle = {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  };

  const videoRowStyle = {
    display: "flex",
    gap: "1rem",
  };

  const videoStyle = {
    width: "50%",
    aspectRatio: "16 / 9",
    borderRadius: "0.5rem",
    objectFit: "cover",
  };

  const textStyle = {
    fontSize: "0.875rem",
    color: "hsl(var(--foreground))",
    lineHeight: "1.6",
  };  

  return (
    <div style={containerStyle}>
      <div style={videoRowStyle}>
        <video
          src={props.sideUrl}
          style={videoStyle}
          autoPlay
          loop
          muted
          playsInline
        />
        <video
          src={props.frontUrl}
          style={videoStyle}
          autoPlay
          loop
          muted
          playsInline
        />
      </div>

    </div>
  );
}
