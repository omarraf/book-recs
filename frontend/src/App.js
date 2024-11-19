import React, { useState } from "react";
import axios from "axios";

function App() {
  // State variables
  const [query, setQuery] = useState(""); // User input
  const [data, setData] = useState(null); // Recommendations from the backend
  const [error, setError] = useState(""); // Error message
  const [loading, setLoading] = useState(false); // Loading state

  // Function to fetch recommendations
  const fetchRecommendations = async () => {
    if (!query) {
      setError("Please enter a query");
      return;
    }

    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/recommend?q=${query}`);
      setData(response.data);
    } catch (err) {
      setError("Failed to fetch recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>Book Recommender</h1>
      <p>Enter a book title, topic, or author to get recommendations:</p>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., Harry Potter, Fantasy, J.K. Rowling"
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

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div>
          <h2>Primary Recommendations</h2>
          {data.primary_recs.map((book, index) => (
            <div key={index} style={{ marginBottom: "20px", borderBottom: "1px solid #ddd", padding: "10px" }}>
              <h3>{book.title}</h3>
              <p><strong>Authors:</strong> {book.author.join(", ") || "N/A"}</p>
              <p><strong>Categories:</strong> {book.categories ? book.categories.join(", ") : "N/A"}</p>
              <p><strong>Description:</strong> {book.description}</p>
              {book.thumbnail && <img src={book.thumbnail} alt={book.title} style={{ maxWidth: "100px" }} />}
            </div>
          ))}

          <h2>Related Recommendations</h2>
          {data.related_recs.map((book, index) => (
            <div key={index} style={{ marginBottom: "20px", borderBottom: "1px solid #ddd", padding: "10px" }}>
              <h3>{book.title}</h3>
              <p><strong>Authors:</strong> {book.author.join(", ") || "N/A"}</p>
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
