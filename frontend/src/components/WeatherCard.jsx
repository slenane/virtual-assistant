import React from "react";

const WeatherCard = ({ weather }) => {
  return (
    <div className="bg-blue-100 p-4 rounded-xl shadow-md w-full max-w-sm">
      <h2 className="text-lg font-semibold mb-2">Weather</h2>
      <p>{weather}</p>
      {/* <p className="text-sm text-gray-600">{weather.temperature}°C</p> */}
    </div>
  );
};

export default WeatherCard;
