/* eslint-disable no-undef */
import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [productName, setProductName] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    chrome.storage.sync.get(['products', 'productName'], function (result) {
      if (result?.products) {
        setProducts(result.products);
      }
      if (result?.productName) {
        setProductName(result.productName);
      }
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await axios.get(`http://localhost:8000/fetchProducts/?product_name=${productName}`, {
        credentials: 'include'
      });
      chrome.storage.sync.set({ 'products': result.data, 'productName': productName }, function () {
        setProducts(result.data);
        console.log(result.data);
        setLoading(false);
      });
    } catch (err) {
      setError("Failed to fetch products. Please try again.");
      setLoading(false);
    }
  }

  return (
    <>
      {products.length > 0 ? (
        <>
          <h2>Product Results</h2>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Price</th>
                <th>Rating</th>
                <th>Image</th>
                <th>URL</th>
                <th>Platform</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product, index) => (
                <tr key={index}>
                  <td>{product.Title}</td>
                  <td>{product.Price}</td>
                  <td>{product.Rating}</td>
                  <td><img src={product.Image} alt={product.Title} width="50" /></td>
                  <td><a href={product.URL} target="_blank" rel="noopener noreferrer">Link</a></td>
                  <td>{product.Platform}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <>
          <h2>Search for the product</h2>
          <form onSubmit={handleSubmit}>
            <input 
              type="text" 
              value={productName} 
              onChange={event => setProductName(event.target.value)} 
              required 
            />
            <button type="submit">Search</button>
          </form>
        </>
      )}

      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
    </>
  )
}

export default App;
