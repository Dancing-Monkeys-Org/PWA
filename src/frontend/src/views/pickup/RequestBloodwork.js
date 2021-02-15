import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Button, makeStyles, Box, Snackbar } from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';

const useStyles = makeStyles((theme) => ({
    button: {
      marginBottom: 10,
    },
  }));

const RequestBloodwork = ({ className, standard_test_id, patient_id, ...rest }) => {
    const classes = useStyles();
    const [alertOpen, setOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertType, setAlertType] = useState("");
    const [buttonDisplay, setButtonDisplay] = useState('inline');

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpen(false);
    };

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    const handleClick = () => {
        fetch('https://dancingmonkeys.tech/api/bloodwork/request?message=pogg&patient_id=' + patient_id + '&standard_test_id=' + standard_test_id , { 
              method: 'POST',
              headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
              }
        })
        .then(response => {
            if(response.status === 200) {
                setAlertType("success");
                setAlertMessage("Test Successfully Requested.")
                setOpen(true);
                setButtonDisplay('none');
            }else {
                setAlertType("error");
                setAlertMessage("Error Occured Requesting Test.")
                setOpen(true);
            }
        })
    }

    return (
        <Box mb={1}>
            <Box display={buttonDisplay}>
                <Button variant="contained" color="primary" onClick={() => {handleClick()}}>Request Test</Button>
            </Box>

            <Snackbar open={alertOpen} autoHideDuration={2000} onClose={handleClose}>
                <MuiAlert elevation={6} variant="filled" onClose={handleClose} severity={alertType}>
                    {alertMessage}
                </MuiAlert>
        </Snackbar>
        </Box>
    );
  };
  
  RequestBloodwork.propTypes = {
    className: PropTypes.string,
    standard_test_id: PropTypes.string.isRequired,
    patient_id: PropTypes.string.isRequired,
  };
  
  export default RequestBloodwork;