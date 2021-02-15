import React, { useState } from 'react';
import PropTypes from 'prop-types';
import TestName from './TestName';
import { Divider } from '@material-ui/core';
import RequestBloodwork from './RequestBloodwork'

const PrescriptionTests = ({ className, pickup_id, patient_id, ...rest }) => {
    const [requirements, updateRequirements] = useState({ is_authorised: "" });

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/pickup/authorised?pickup_id=' + pickup_id, { 
              headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
              }
            })
            .then(response => response.json())
            .then(data => {
                updateRequirements(data);
            });
      }, [pickup_id]);

    return (
        <div>
        <h4>Pickup Authorised: {requirements.is_authorised === undefined ? "" : requirements.is_authorised.toString()}</h4>
        <Divider></Divider>
        <div>
            {requirements.requirements !== undefined ? 
                requirements.requirements.map((test) => 
                    <div>
                        <h3><TestName test_id={test.test_id}/></h3>
                        <h5>Last Required Test Date: {test.minimum_last_test_date}</h5>
                        <h5>Requirement Met: {test.requirement_met}</h5>
                        {test.requirement_met === 'No' ? <RequestBloodwork patient_id={patient_id} standard_test_id={test.test_id}></RequestBloodwork> : ""}
                        <Divider></Divider>
                    </div>
                )
                : "Loading Tests..."
            }
        </div>
        </div>
    );
  };
  
  PrescriptionTests.propTypes = {
    className: PropTypes.string,
    pickup_id: PropTypes.string.isRequired
  };
  
  export default PrescriptionTests;