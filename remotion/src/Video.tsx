import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: "clamp"});
  return (
    <AbsoluteFill style={{backgroundColor: "#111", color: "white", justifyContent: "center", alignItems: "center", fontFamily: "Arial", opacity}}>
      <h1>Creador YouTube</h1>
      <p>Open-source video factory</p>
    </AbsoluteFill>
  );
};
