import React, { useState } from 'react';
import PropTypes from 'prop-types';

const Patient = ({ className, patient_id, ...rest }) => {
    const [patient, updatePatient] = useState([]);

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/patient?patient_id=' + patient_id, { 
              headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
              }
            })
            .then(response => response.json())
            .then(data => {
                updatePatient(data);
            });
      }, [patient_id]);

    return (
        <div className={className}>
            <h4>{patient.forename} {patient.surname}</h4>
            <h4>{patient.sex}</h4>
            <h4>{patient.age} Years Old</h4>
        </div>
    );
  };
  
  Patient.propTypes = {
    className: PropTypes.string,
    patient: PropTypes.object.isRequired
  };
  
  export default Patient;