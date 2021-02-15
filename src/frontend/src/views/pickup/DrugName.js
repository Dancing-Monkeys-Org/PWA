import React, { useState } from 'react';
import PropTypes from 'prop-types';

const DrugName = ({ className, drug_id, ...rest }) => {
    const [drug, updateDrug] = useState([]);

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/drug?drug_id=' + drug_id, { 
              headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
              }
            })
            .then(response => response.json())
            .then(data => {
                updateDrug(data);
            });
      }, [drug_id]);

    return (
        <h4>{drug.name}</h4>
    );
  };
  
  DrugName.propTypes = {
    className: PropTypes.string,
    drug_id: PropTypes.object.isRequired
  };
  
  export default DrugName;