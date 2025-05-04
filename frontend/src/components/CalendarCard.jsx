import React from "react";

const EventCard = ({ events }) => {
  return (
    <div className="bg-green-100 p-4 rounded-xl shadow-md w-full max-w-sm">
      <h2 className="font-semibold text-lg mb-3">Today's Events</h2>
      {events.length === 0 ? (
        <p className="text-sm text-gray-500">No events for today.</p>
      ) : (
        <ul className="space-y-2">
          {events.map((event, index) => (
            <li key={index} className="bg-white p-3 rounded shadow">
              <p className="text-sm text-gray-600">{event}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default EventCard;
