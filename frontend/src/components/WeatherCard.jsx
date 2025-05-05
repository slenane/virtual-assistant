import React from "react";

const WeatherCard = ({ weather }) => {
  const date = new Date();
  const formattedDate = date.toLocaleDateString("en-GB", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  return (
    <div class=" flex items-center">
      <div class="flex flex-col bg-white rounded p-4 w-full max-w-xs">
        <div class="font-bold text-xl">{weather.name}</div>
        <div class="text-sm text-gray-500">{formattedDate}</div>
        <div class="self-center inline-flex items-center justify-center rounded-lg h-24 w-24">
          <img
            src={`http://openweathermap.org/img/wn/${weather.icon}@2x.png`}
            alt={weather.description}
          />
        </div>
        <div class="flex flex-row items-center justify-center mt-6">
          <div class="font-medium text-6xl">{weather.temp}°</div>
          <div class="flex flex-col items-center ml-6">
            <div>{weather.description}</div>
            <div class="mt-1">
              <span class="text-sm">
                <i class="far fa-long-arrow-up"></i>
              </span>
              <span class="text-sm font-light text-gray-500">
                {weather.temp_max}°C
              </span>
            </div>
            <div>
              <span class="text-sm">
                <i class="far fa-long-arrow-down"></i>
              </span>
              <span class="text-sm font-light text-gray-500">
                {weather.temp_min}°C
              </span>
            </div>
          </div>
        </div>
        <div class="flex flex-row justify-between mt-6">
          <div class="flex flex-col items-center">
            <div class="font-medium text-sm">Wind</div>
            <div class="text-sm text-gray-500">{weather.wind}k/h</div>
          </div>
          <div class="flex flex-col items-center">
            <div class="font-medium text-sm">Humidity</div>
            <div class="text-sm text-gray-500">{weather.humidity}%</div>
          </div>
          <div class="flex flex-col items-center">
            <div class="font-medium text-sm">Visibility</div>
            <div class="text-sm text-gray-500">{weather.visibility}km</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
