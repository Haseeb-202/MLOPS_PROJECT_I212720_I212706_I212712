import React, { useState } from 'react';
import axios from 'axios';

function WeatherPredictor({ setUserToken }) {
  const [weatherData, setWeatherData] = useState({
    temperature: '',
    humidity: '',
    pressure: ''
  });

  const handleChange = (event) => {
    setWeatherData({
      ...weatherData,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('userToken');  // Assuming the token is stored in local storage
    if (!token) {
      alert('No token found, please log in again.');
      setUserToken(null);
      return;
    }
    
    try {
      const response = await axios.post('http://localhost:5000/predict', weatherData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log("Prediction Result:", response.data);
      alert(`Predicted result: ${JSON.stringify(response.data)}`);
    } catch (error) {
      console.error("Error during prediction:", error.response ? error.response.data : error.message);
      if (error.response && error.response.status === 401) {
        // Handle token expiration or unauthorized access
        setUserToken(null);
        localStorage.removeItem('userToken'); // Clear the stored token
        alert('Session expired, please log in again.');
      }
    }
  };

  return (
    <div>
      <h1>Weather Predictor</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="temperature" placeholder="Enter temperature (°C)" value={weatherData.temperature} onChange={handleChange} />
        <input type="text" name="humidity" placeholder="Enter humidity (%)" value={weatherData.humidity} onChange={handleChange} />
        <input type="text" name="pressure" placeholder="Enter pressure (hPa)" value={weatherData.pressure} onChange={handleChange} />
        <button type="submit">Predict Temperature</button>
      </form>
      <button onClick={() => {
        setUserToken(null);
        localStorage.removeItem('userToken');
      }}>Logout</button>
    </div>
  );
}

export default WeatherPredictor;
