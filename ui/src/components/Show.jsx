import React, { useState } from 'react';

function TextWithExpand(props) {
  let { text, maxLength, className} = props;
  className = `${className || ""}`;
  const [expanded, setExpanded] = useState(false);

  if (text.length <= maxLength) {
    return <p className={className}>{text}</p>;
  }

  const displayedText = expanded ? text : text.substring(0, maxLength) + '...';

  return (
    <div className={className}>
      <p>{displayedText}</p>
      <button onClick={() => setExpanded(!expanded)} className="bg-gray-300 p-2 rounded">
        {expanded ? 'Read less' : 'Read more'}
      </button>
    </div>
  );
}

export default function Show(props) {
  let {
    name,
    description,
    className,
    length: { seasons, episodes },
  } = props;
  className = `bg-gray-200 p-4 rounded ${className || ""}`;
  return (
    <div className={className}>
      <p className="font-bold">
        {name} ({seasons} seasons x {episodes} episodes)
      </p>
      <p>
        <span className="font-bold">Networks:</span> {props.networks.join(", ")}
      </p>
      <p>
        <span className="font-bold">Genres:</span> {props.genres.join(", ")}
      </p>
      <TextWithExpand text={description} maxLength={200} className="mt-4" />
    </div>
  );
}

