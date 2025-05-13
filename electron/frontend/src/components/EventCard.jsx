import React from "react";

const EventCard = ({ events }) => {
  return (
    <div className="flex flex-col bg-white rounded p-4 w-full max-w-xs">
      <h2 className="font-semibold text-lg text-black mb-3">Today's Events</h2>
      <div className="px-2">
        {events.length === 0 ? (
          <p className="text-sm text-gray-500">No events for today.</p>
        ) : (
          events.map((event, index) => (
            <div className="border-b pb-4 border-gray-400 border-dashed">
              <p className="text-xs leading-3 text-gray-700">
                {event.start_time} - {event.end_time}
              </p>
              <p
                tabindex="0"
                className="focus:outline-none text-lg font-medium leading-5 text-black mt-2"
              >
                {event.summary}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventCard;
