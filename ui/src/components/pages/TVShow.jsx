import { useState, useEffect } from "react";
import Page from "./Page";
import { api } from "../../services/bootstrap";
import Show from "../Show";

function SearchBar(props) {
  let {
    value,
    placeholder = "Search...",
    onChange,
    onSubmit,
    onClear,
    locked,
    className,
  } = props;
  className = `${className || ""} bg-gray-200 p-2 rounded flex`;
  onChange = onChange || function () {};
  onSubmit = onSubmit || function () {};
  onClear = onClear || function () {};

  return (
    <div className={className}>
      <input
        placeholder={placeholder}
        disabled={locked}
        type="text"
        value={value}
        className="w-full mr-1"
        onChange={(e) => {
          onChange(e);
        }}
        onKeyDown={(e) => {
          console.log(e.key);
          if (e.key === "Enter") {
            onSubmit();
          }
        }}
      />

      <button
        className="bg-gray-400 px-2 rounded text-white"
        onClick={onClear}
        disabled={!value}
        title="Clear"
      >
        Clear
      </button>
    </div>
  );
}

export default function TVShow(props) {
  const [shows, setShows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeframe, setTimeframe] = useState("day");
  const [query, setQuery] = useState("");
  const [querySent, setQuerySent] = useState(false);

  useEffect(() => {
    api
      .trending(timeframe)
      .then(setShows)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [timeframe]);
  let searchBar = (
    <SearchBar
      className="ml-2 mb-2"
      placeholder="Search for Show..."
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onSubmit={() => {
        setShows([]);
        setLoading(true);
        setQuerySent(true);
        api
          .search(query)
          .then(setShows)
          .catch(setError)
          .finally(() => {
            setLoading(false);
          });
      }}
      onClear={() => {
        setQuerySent(false);
        setQuery("");
        setShows([]);
        setLoading(true);
        api
          .trending(timeframe)
          .then(setShows)
          .catch(setError)
          .finally(() => setLoading(false));
      }}
    />
  );
  let children;
  if (loading) {
    children = <p>Loading...</p>;
  } else if (error) {
    children = <p> Failed to communicate with server :(</p>;
  } else if (query && shows && querySent) {
    children = (
      <div>
        <h2 className="text-2xl font-bold my-4 ml-2">
          Search Results for "{query}":
        </h2>
        {searchBar}
        <div className="flex flex-wrap">
          {shows.map((show, index) => {
            return (
              <Show
                className="m-2 xl:w-[20%] md:mx-1 md:w-[48%] sm:w-full"
                key={index}
                {...show}
              />
            );
          })}
        </div>
      </div>
    );
  } else {
    children = (
      <div>
        <h2 className="text-2xl font-bold my-4 ml-2">
          Trending TV Shows:{" "}
          <select
            value={timeframe}
            onChange={(e) => {
              setShows([]);
              setLoading(true);
              setTimeframe(e.target.value);
            }}
          >
            <option value="day">Today</option>
            <option value="week">This Week</option>
          </select>
        </h2>
        {searchBar}
        <div className="flex flex-wrap">
          {shows.map((show, index) => {
            return (
              <Show
                className="m-2 xl:w-[20%] md:mx-1 md:w-[48%] sm:w-full"
                key={index}
                {...show}
              />
            );
          })}
        </div>
      </div>
    );
  }
  return <Page title="Discover TV!!">{children}</Page>;
}
