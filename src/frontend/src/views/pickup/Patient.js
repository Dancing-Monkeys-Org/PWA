import React, { useState } from 'react';
import PropTypes from 'prop-types';

const Patient = ({ className, patient, ...rest }) => {
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
      }, []);

    return (
        <h4>{drug.name}</h4>
    );
  };
  
  Patient.propTypes = {
    className: PropTypes.string,
    patient: PropTypes.object.isRequired
  };
  
  export default Patient;