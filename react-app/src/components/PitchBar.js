import React, { useEffect, useState } from "react";
import './PitchRungs.css';

const PitchBar = ({ pitch }) => {
  const [height, setHeight] = useState(0);

  useEffect(() => {
    // Calculate the height based on the pitch. This is a simple example and should be adjusted.
    // Assuming the pitch range is from 0 to 100 and height range is from 0% to 100%.
    const newHeight = Math.min(Math.max(pitch, 0), 100);
    setHeight(newHeight);
  }, [pitch]);

  return (
    <div className="white-pitch-bar" style={{ height: `${height}%` }}></div>
  );
};

export default PitchBar;
