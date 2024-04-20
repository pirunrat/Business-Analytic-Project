import '../css/DataTable.css';
import React from 'react';

function DataTable({ data }) {
  const keyName = {
    'AGE': 'Age',
    'ASSET_COST': 'Cost of the Asset',
    'CREDIT_HISTORY_LENGTH': 'Duration of credit history',
    'DISBURSED_AMOUNT': 'Disbursed Amount',
    'NO_OF_INQUIRIES': 'Number of Quiries',
    'PERFORM_CNS_SCORE_DESCRIPTION': 'Bureau Score Type',
    'LTV': 'Loan to Value Percentage'
  };

  const PerformanceDescription = {
    5: 'Very High',
    4: 'High',
    3: 'Medium',
    2: 'Low',
    1: 'Very Low'
  };

  return (
    <div className="data-table">
      {Object.entries(data).map(([key, value]) => (
        <div key={key} className="data-row">
          <div className="data-key">{keyName[key]}</div>
          <div className="data-value">
            {key === 'PERFORM_CNS_SCORE_DESCRIPTION' ? PerformanceDescription[value] : value}
          </div>
        </div>
      ))}
    </div>
  );
}

export default DataTable;
