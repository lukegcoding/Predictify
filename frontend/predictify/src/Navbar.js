import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="Navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/schedule">Schedule</Link></li>
        <li><Link to="/future-work">Future Work</Link></li>
        <li><Link to="/games">Games</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
