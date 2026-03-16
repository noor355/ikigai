import axios from "axios";
import { useEffect, useState } from "react";

function App() {

  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/")
      .then(res => setMessage(res.data.message));
  }, []);

  return (
    <div>
      <h1>AI Career Discovery Platform</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;