import React from "react";
import './PitchRungs.css';

const PitchRungs = () => {
  const scalePattern = ['whole', 'whole', 'whole', 'half', 'whole', 'whole', 'whole', 'half', 'whole'];
  // The last element in this array is a design feature for cleaner code

  return (
    <div className="pitch-rungs">
      {scalePattern.map((step, index) => (
        <div key={index} className={`line ${step}-step`}></div>
      ))}
    </div>
  );
};

export default PitchRungs;
