import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Login from './Login';
import Register from './Register';
import WeatherPredictor from './WeatherPredictor'; // This will be your weather prediction component

function App() {
  const [userToken, setUserToken] = useState(null);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          {!userToken ? (
            <Routes>
              <Route path="/" element={<Login setUserToken={setUserToken} />} />
              <Route path="/register" element={<Register />} />
            </Routes>
          ) : (
            <WeatherPredictor setUserToken={setUserToken} />
          )}
        </header>
      </div>
    </Router>
  );
}

export default App;
