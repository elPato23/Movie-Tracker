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
    poster,
  } = props;

  poster = poster || {
    small: "/images/small/0_poster.png",
    medium: "/images/medium/0_poster.png",
    large: "/images/large/0_poster.png",
  }
  let { small: poster_sm, medium: poster_md, large: poster_lg } = poster;
  className = `bg-gray-200 p-4 rounded ${className || ""} relative text-white`;
  return (
    <div className={className}>
      <picture>
        <source srcSet={poster_sm} media='(max-width: 600px)'/>
        <source srcSet={poster_md} media='(max-width: 900px)'/>
        <source srcSet={poster_lg} media='(min-width: 901px)'/>
        <img className='w-full rounded' src={poster_sm} alt={name} />
      </picture>
      <div className='absolute rounded hover:opacity-80 transition duration-200 ease-in  top-0 right-0 opacity-0 bg-gray-800 p-4 h-full flex flex-col'>
        <span className="flex-2"></span>
        <p className="font-bold">
          {name} ({seasons} seasons x {episodes} episodes)
        </p>
        <p>
          <span className="font-bold">Networks:</span> {props.networks.join(", ")}
        </p>
        <p>
          <span className="font-bold">Genres:</span> {props.genres.join(", ")}
        </p>
        <TextWithExpand text={description} maxLength={200} className="mt-4 flex-1" />
      </div>
    </div>
  );
}

