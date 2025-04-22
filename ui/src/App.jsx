import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Home from "./components/pages/Home";
import TVShow from "./components/pages/TVShow";
import image from "./logo512.png";
let navbar = [
  { name: "Home", path: "/" },
  { name: "TV Shows", path: "/tv-shows" },
];

export default function App() {
  return (
    <Router>
      <div>
        <header className="bg-gray-800 flex items-center justify-between p-4">
          <Link to="/">
            <img src={image} className="w-16 h-16" alt="Movie Tracker Logo" />
          </Link>
          <nav className="p-4 text-white w-full">
            <ul className="flex space-x-4">
              {navbar.map((item, index) => {
                return (
                  <li key={index} className="mr-4">
                    <Link
                      to={item.path}
                      className="text-white hover:text-gray-300 hover:bg-gray-700 py-2 px-4 rounded transition duration-300 ease-in-out"
                    >
                      {item.name}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>
        </header>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
          <Route path="/tv-shows" Component={TVShow} />
          <Route path="/" Component={Home} />
        </Routes>
      </div>
    </Router>
  );
}
