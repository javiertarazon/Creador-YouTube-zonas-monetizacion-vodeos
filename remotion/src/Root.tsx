import React from "react";
import { Composition } from "remotion";
import { Video, VideoProps } from "./Video";

export const Root: React.FC = () => (
  <Composition<VideoProps>
    id="Video"
    component={Video}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={1800}
    defaultProps={{
      title: "Creador YouTube",
      topic: "Open-source video factory",
      script: "",
      duration_seconds: 60,
      assets: [],
      voice_audio: null,
    }}
    calculateMetadata={({ props }) => ({
      durationInFrames: Math.max(30, Math.round(props.duration_seconds * 30)),
    })}
  />
);
