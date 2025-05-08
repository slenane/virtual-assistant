import { useEffect, useState } from "react";

const useGeolocation = () => {
  const [location, setLocation] = useState({ latitude: null, longitude: null });

  useEffect(() => {
    const getLocation = async () => {
      // Fallback to IP-based location (might not work with vpns)
      try {
        const res = await fetch("http://ip-api.com/json");
        const data = await res.json();
        setLocation({ latitude: data.lat, longitude: data.lon });
      } catch (e) {
        console.error("IP fallback failed:", e);
      }

      // This doesn't work right now
      // if ("geolocation" in navigator) {
      //   navigator.geolocation.getCurrentPosition(
      //     (position) => {
      //       const { latitude, longitude } = position.coords;
      //       console.log(latitude, longitude);
      //       setLocation({ latitude, longitude });
      //     },
      //     async (error) => {
      //       console.error("Geolocation error: ", error.message);

      //       // Fallback to IP-based location
      //       try {
      //         const res = await fetch("http://ip-api.com/json");
      //         const data = await res.json();
      //         setLocation({ latitude: data.lat, longitude: data.lon });
      //       } catch (e) {
      //         console.error("IP fallback failed:", e);
      //       }
      //     }
      //   );
      // } else {
      //   console.log("Geolocation not supported");
      // }
    };

    getLocation();
  }, []);

  return location;
};

export default useGeolocation;
