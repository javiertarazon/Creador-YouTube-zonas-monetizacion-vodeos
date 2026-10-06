import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export type VideoProps = {
  title: string;
  topic: string;
  script: string;
  duration_seconds: number;
  assets: Array<{ public_name?: string; path?: string }>;
  voice_audio?: string | null;
};

const Card: React.FC<{ title: string; topic: string }> = ({ title, topic }) => (
  <AbsoluteFill
    style={{
      background: "linear-gradient(135deg, #0f172a, #1e293b)",
      color: "white",
      justifyContent: "center",
      alignItems: "center",
      padding: 100,
      fontFamily: "Arial, sans-serif",
    }}
  >
    <div style={{ width: "82%", textAlign: "center" }}>
      <div style={{ fontSize: 38, opacity: 0.7, marginBottom: 32 }}>CREADOR YOUTUBE</div>
      <h1 style={{ fontSize: 86, lineHeight: 1.05, margin: 0 }}>{title}</h1>
      <p style={{ fontSize: 48, color: "#cbd5e1" }}>{topic}</p>
    </div>
  </AbsoluteFill>
);

export const Video: React.FC<VideoProps> = (props) => {
  const frame = useCurrentFrame();
  const duration = Math.max(30, Math.round(props.duration_seconds * 30));
  const fade = interpolate(frame, [0, 24, duration - 24, duration], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const scriptPreview = props.script.slice(0, 320);
  return (
    <AbsoluteFill style={{ backgroundColor: "#020617", opacity: fade }}>
      <Card title={props.title} topic={props.topic} />
      <Sequence from={Math.floor(duration * 0.18)} durationInFrames={Math.floor(duration * 0.64)}>
        <AbsoluteFill
          style={{
            backgroundColor: "rgba(2,6,23,0.88)",
            color: "white",
            justifyContent: "center",
            padding: 150,
            fontFamily: "Arial, sans-serif",
          }}
        >
          <h2 style={{ fontSize: 54 }}>Guion</h2>
          <p style={{ fontSize: 38, lineHeight: 1.35 }}>{scriptPreview}</p>
        </AbsoluteFill>
      </Sequence>
      {props.voice_audio ? <Audio src={staticFile(props.voice_audio)} /> : null}
    </AbsoluteFill>
  );
};
