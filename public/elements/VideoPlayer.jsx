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
    color: "white", 
    lineHeight: "1.6",
  };

  return (
    <div style={containerStyle}>
      {/* 并排视频 */}
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

      {/* 文本区域 */}
      <div style={textStyle}>
        <p>
          <strong>Note：</strong> {props.notes || "请保持正确姿势，避免身体摇晃。"}
        </p>
        <p style={{ marginTop: "0.5rem" }}>
          <strong>Tips：</strong> {props.tips || "收紧肩胛骨，保持核心稳定。"}
        </p>
      </div>
    </div>
  );
}
