/* eslint-disable no-undef */
import { useState, useEffect } from 'react';
import axios from 'axios';
// import './App.css';

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
        setProductName("");
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
        if(result.data.length==0){
          setError("No Products Found.");
        }
      });
    } catch (err) {
      setProductName("");
      setError("Failed to fetch products. Please try again.");
      setLoading(false);
    }
  }

  const handleClear = () => {
    chrome.storage.sync.set({ 'products': "", 'productName': "" }, function () {
      setProducts("");
      setProductName("");
      setLoading(false);
    });
  }

  return (
    <>
      {products.length > 0 ? (
        <>
          <div className="flex flex-col justify-center items-center w-96">
            <span className="text-3xl m-3">Product Results</span>
            <table className="table-auto w-full">
              <thead>
                <tr>
                  <th>Image</th>
                  <th className="w-1/2">Details</th>
                  <th>URL</th>
                  <th>Platform</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product, index) => (
                  <tr key={index} className="border-b">
                    <td className="p-2"><img src={product.Image} alt={product.Title} width="50" /></td>
                    <td className="p-2">
                      <div className="flex flex-col">
                        <span className="text-amber-950">{product.Title}</span>
                        <div className="flex flex-row justify-between my-2">
                          <i className="fa fa-inr" aria-hidden="true"><span>{" "+product.Price+"/-"}</span></i>
                          <i className="fa fa-star" aria-hidden="true"><span>{product.Rating}</span></i>
                        </div>
                        
                      </div>
                    </td>
                    <td className="p-2"><a href={product.URL} target="_blank" rel="noopener noreferrer">Link</a></td>
                    <td className="p-2">{product.Platform}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button onClick={handleClear} className=" px-3 py-1 m-1 border-solid border-2 border-stone-800 rounded">Clear</button>
          </div>
        </>
      ) : (
        <>
        <div className="flex flex-col justify-center items-center m-3 w-96">
          <h2 className="text-3xl m-4">Search for the product</h2>
          <form onSubmit={handleSubmit} className="m-2">
            <input 
              type="text" 
              value={productName} 
              onChange={event => setProductName(event.target.value)}
              placeholder='Enter the Product...' 
              required 
              className="w-60 h-6 border-solid border-2 border-stone-800"
            />
            <button type="submit" className=" px-3 py-1 m-1 border-solid border-2 border-stone-800 rounded">Search</button>
          </form>
          {loading && <span>Loading...</span>}
          {error && <span>{error}</span>}
          </div>
        </>
      )}

    </>
  )
}

export default App;
