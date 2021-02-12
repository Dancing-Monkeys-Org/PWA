import React, { useState } from 'react';
import PropTypes from 'prop-types';

const DrugName = ({ className, drug_id, ...rest }) => {
    const [drug, updateDrug] = useState([]);

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/drug?drug_id=' + drug_id, { 
              headers:  {
                'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTMxNDMyNDcsImV4cCI6MTYxMzIyOTY0NywianRpIjoiZDA0YzRhMmYtMTY3ZC00NzFjLWJlODYtOGJlY2FlZDA1OTBkIiwiaWQiOiIzYzc2YmJlNy0xNTJkLTQ5N2UtYWY4Yi02ZTkzNTMyYmJlZWEiLCJybHMiOiIiLCJyZl9leHAiOjE2MTU3MzUyNDd9.lqxCRYdxSVPEJfXfcb5mMoVm_f29VqsA9xHFyAfOWfY',
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
  
  DrugName.propTypes = {
    className: PropTypes.string,
    drug_id: PropTypes.object.isRequired
  };
  
  export default DrugName;