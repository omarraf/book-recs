import React, { useState } from "react";
import axios from "axios";

function App() {
  // State variables
  const [query, setQuery] = useState(""); // User's search input
  const [recommendations, setRecommendations] = useState([]); // Recommendation results
  const [error, setError] = useState(""); // Error messages
  const [loading, setLoading] = useState(false); // Loading state

  // Function to fetch recommendations
  const fetchRecommendations = async () => {
    if (!query) {
      setError("Please enter a book name.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/recommend?q=${query}`);
      setRecommendations(response.data);
    } catch (err) {
      setError("Failed to fetch recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Function to refresh recommendations
  const handleRefresh = async () => {
    if (!query) {
      setError("Please search for a book first.");
      return;
    }
    await fetchRecommendations(); // Just re-fetch recommendations
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>BookRecs</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter a book name"
        style={{
          padding: "10px",
          width: "300px",
          marginRight: "10px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      />
      <button
        onClick={fetchRecommendations}
        style={{
          padding: "10px 20px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Search
      </button>
      <button
        onClick={handleRefresh}
        style={{
          padding: "10px 20px",
          backgroundColor: "#28a745",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          marginLeft: "10px",
        }}
      >
        Refresh
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {recommendations.length > 0 && (
        <div>
          <h2>Recommendations</h2>
          {recommendations.map((book, index) => (
            <div key={index} style={{ marginBottom: "20px", borderBottom: "1px solid #ddd", padding: "10px" }}>
              <h3>{book.title}</h3>
              <p><strong>Author(s):</strong> {book.author.join(", ") || "Unknown"}</p>
              <p><strong>Description:</strong> {book.description}</p>
              {book.thumbnail && <img src={book.thumbnail} alt={book.title} style={{ maxWidth: "100px" }} />}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
