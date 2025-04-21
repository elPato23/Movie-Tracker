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
      <p className="my-2">{description}</p>
    </div>
  );
}
