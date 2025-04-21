import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Home from "./components/pages/Home";
import TVShow from "./components/pages/TVShow";

let navbar = [
  { name: "Home", path: "/" },
  { name: "TV Shows", path: "/tv-shows" },
];

export default function App() {
  return (
    <Router>
      <div>
        <nav className="bg-gray-800 p-4 text-white">
          <ul className="flex space-x-4">
            {navbar.map((item, index) => {
              return (
                <li key={index} className="mr-4">
                  <Link
                    to={item.path}
                    className="text-white hover:text-gray-300 hover:bg-gray-700 py-2 px-4 rounded"
                  >
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

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
