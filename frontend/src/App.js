import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import DataTable from './components/DataTable';

function App() {
  const [formData, setFormData] = useState({ query: '' });
  const [data, setData] = useState(null);
  const [rawdata, setRawdata] = useState('');
  const [isLoading, setIsLoading] = useState(false);


  const backgroundColor = {
    0:'green',
    1:'#bf0303'
  }

  const handleChange = (event) => {
    const { value } = event.target;
    setFormData({ query: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/query', formData);

      if (response) {
        setData(response.data.result);
        setRawdata(response.data.rawdata[0]);
        console.log('Response:', response.data.result);
      }
    } catch (error) {
      console.error('Error:', error);
    }
    setIsLoading(false);
  };

  const result = { 0: 'Low risk', 1: 'High Risk' };

  return (
    <div className="App">
      <nav className="top-bar">
        <div className="container">
          <img src={logo} alt="Logo" className="logo" />
          <h1 className="title">Loan Default Prediction Application</h1>
        </div>

        <div className='Dashboard'> 
          <a href="https://app.powerbi.com/groups/me/reports/194c8db5-cba6-4774-91e3-250330b0c635/ReportSection?experience=power-bi"><h1>Dashboard</h1></a>
        </div>
      </nav>

      <div className="main">
        <div className="card">

            <div className="card-content">
              <form onSubmit={handleSubmit}>
                <label htmlFor="query">Query:</label>
                <input
                  type="text"
                  id="query"
                  name="query"
                  value={formData.query}
                  onChange={handleChange}
                />
                <button type="submit" disabled={isLoading}>
                  {isLoading ? 'Loading...' : 'Submit'}
                </button>
              </form>

              {data && (
                   <div className="result" style={{ backgroundColor:backgroundColor[data] }}>

                   {console.log('Result:', result[data])}
                   <h1>{result[data]}</h1>
                 </div>
                )}
            </div>

            <div className='result-table'>
            <DataTable data={rawdata} />
            </div>

        </div>


      </div>
    </div>
  );
}

export default App;
