import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function Games() {
  const [games, setGames] = useState([]);
  const [filteredGames, setFilteredGames] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/games') // Ensure this endpoint is correct
      .then(response => {
        console.log(response.data); // Log the data to verify it
        setGames(response.data);
        setFilteredGames(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the game data!', error);
      });
  }, []);

  const handleSearch = (event) => {
    setSearch(event.target.value);
    const filtered = games.filter(game =>
      game.home_team.toLowerCase().includes(event.target.value.toLowerCase()) ||
      game.away_team.toLowerCase().includes(event.target.value.toLowerCase())
    );
    setFilteredGames(filtered);
  };

  const handleSort = (key) => {
    const sorted = [...filteredGames].sort((a, b) => {
      if (a[key] < b[key]) return -1;
      if (a[key] > b[key]) return 1;
      return 0;
    });
    setFilteredGames(sorted);
  };

  return (
    <div className="Games">
      <header className="Games-header">
        <h1>NHL Games</h1>
        <input
          type="text"
          placeholder="Search by team"
          value={search}
          onChange={handleSearch}
        />
        <button onClick={() => handleSort('date')}>Sort by Date</button>
        <button onClick={() => handleSort('home_team')}>Sort by Home Team</button>
        <button onClick={() => handleSort('away_team')}>Sort by Away Team</button>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Season</th>
              <th>Game Type</th>
              <th>Venue</th>
              <th>Neutral Site</th>
              <th>Start Time</th>
              <th>Home Team</th>
              <th>Home Team Score</th>
              <th>Away Team</th>
              <th>Away Team Score</th>
              <th>Game State</th>
              <th>Game Center Link</th>
            </tr>
          </thead>
          <tbody>
            {filteredGames.map(game => (
              <tr key={game.game_id}>
                <td>{new Date(game.date).toLocaleDateString()}</td>
                <td>{game.season}</td>
                <td>{game.game_type}</td>
                <td>{game.venue}</td>
                <td>{game.neutral_site}</td>
                <td>{new Date(game.start_time).toLocaleTimeString()}</td>
                <td>{game.home_team}</td>
                <td>{game.home_team_score}</td>
                <td>{game.away_team}</td>
                <td>{game.away_team_score}</td>
                <td>{game.game_state}</td>
                <td><a href={game.game_center_link} target="_blank" rel="noopener noreferrer">Link</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      </header>
    </div>
  );
}

export default Games;
