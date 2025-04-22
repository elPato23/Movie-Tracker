import React from "react";
import Page from "./Page";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <Page title="Home">
      <div className="ml-2">
        <p>Welcome to Movie Tracker!!</p>
        <p>
          Go to <Link to="/tvshows">TV Shows</Link> to see the different shows
          you like.
        </p>
      </div>
    </Page>
  );
}
