import React, { useState } from 'react';
import PropTypes from 'prop-types';

const ContactInfo = ({ className, contact_id, ...rest }) => {
    const [contactInfo, updateContactInfo] = useState([]);

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
    fetch('https://dancingmonkeys.tech/api/contact?contact_id=' + contact_id, { 
            headers:  {
            'Authorization': `Bearer ${token}`,
            'Accept': '*/*'
            }
        })
        .then(response => response.json())
        .then(data => {
            updateContactInfo(data);
        });
    }, [contact_id]);

    return (
        <div className={className}>
            <h4>{contactInfo.phone_number}</h4>
            <h4>{contactInfo.email_address}</h4>
            <h4>{contactInfo.address_line_1}</h4>
            <h4>{contactInfo.address_line_2}</h4>
            <h4>{contactInfo.address_line_3}</h4>
            <h4>{contactInfo.address_line_4}</h4>
            <h4>{contactInfo.postcode}</h4>
        </div>
    );
  };
  
  ContactInfo.propTypes = {
    contactInfo: PropTypes.object.isRequired
  };
  
  export default ContactInfo;