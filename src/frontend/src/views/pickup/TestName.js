import React, { useState } from 'react';
import PropTypes from 'prop-types';

const TestName = ({ className, test_id, ...rest }) => {
    const [test, updateTest] = useState([]);

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/test?test_id=' + test_id, { 
              headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
              }
            })
            .then(response => response.json())
            .then(data => {
                updateTest(data);
            });
      }, [test_id]);

    return (
        <h4>{test.name}</h4>
    );
  };
  
  TestName.propTypes = {
    className: PropTypes.string,
    test_id: PropTypes.object.isRequired
  };
  
  export default TestName;