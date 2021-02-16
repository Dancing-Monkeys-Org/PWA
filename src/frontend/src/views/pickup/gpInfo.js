import React, { useState } from 'react';
import PropTypes from 'prop-types';

const GpInfo = ({ className, gp_id, ...rest }) => {
    const [gpInfo, updategpInfo] = useState([]);

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
    fetch('https://dancingmonkeys.tech/api/gp?gp_id=' + gp_id, { 
            headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
            }
        })
        .then(response => response.json())
        .then(data => {
            updategpInfo(data);
        });
    }, [gp_id]);

    return (
        <div className={className}>
            <h4>{gpInfo.name}</h4>
        </div>
    );
  };
  
  GpInfo.propTypes = {
    gpInfo: PropTypes.object.isRequired
  };
  
  export default GpInfo;