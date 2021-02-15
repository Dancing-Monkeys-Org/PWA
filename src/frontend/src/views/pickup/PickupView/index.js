import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Container,
  Divider,
  makeStyles,
  Typography,
  Select,
  InputLabel,
  Snackbar
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';
import FormControl from '@material-ui/core/FormControl';
import Page from 'components/Page';
import Patient from '../Patient'
import DrugName from '../DrugName';
import PrescriptionTests from '../PrescriptionTests';

const useStyles = makeStyles((theme) => ({
    formControl: {
      marginLeft: 10,
      minWidth: 120,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
    root: {
      backgroundColor: theme.palette.background.dark,
      minHeight: '100%',
      paddingBottom: theme.spacing(3),
      paddingTop: theme.spacing(3)
    },
    productCard: {
      height: '100%'
    }
  }));

const PickupView = () => { 
    const classes = useStyles();
    const {id} = useParams();
    const [pickup, updatePickup] = useState([]);
    const [alertOpen, setAlertOpen] = useState(false);
    const [alertType, setAlertType] = useState("info");
    const [alertMessage, setAlertMessage] = useState("Info");

    const loginVal = JSON.parse(localStorage.getItem("login"));
    const token = loginVal.token;

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/pickup?pickup_id=' + id.toString(), { 
            headers:  {
                'Authorization': `Bearer ${token}`,
                'Accept': '*/*'
            }
            })
            .then(response => response.json())
            .then(data => {
              updatePickup(data);
            });
    }, []);

    const handleChange = (event) => {
      let success = false;

      fetch('https://dancingmonkeys.tech/api/pickup/status?pickup_id=' + id.toString(), {
          method: 'PATCH',
          body: JSON.stringify({
            status: event.target.value
          }),
          headers: {
            'Authorization': `Bearer ${token}`,
            "Content-type": "application/json; charset=UTF-8"
          }
      })
      .then(response => response.json())
      .then(json => {
        if(json.status_code !== undefined){
            console.log("CODEEEE: " + json.status_code)
            if(json.status_code == 401) {
              setAlertMessage("Unauthorised! Must have Pharmacist Role to Update Status");
              setAlertType("error");
              setAlertOpen(true);
            }
            else if(json.status_code == 400) {
              setAlertMessage("Cannot update status as pickup has unmet requirements");
              setAlertType("error");
              setAlertOpen(true);
            } else { 
              setAlertMessage("An unknown error has occured, please try again later.");
              setAlertType("error");
              setAlertOpen(true);
            }
        }else {
          setAlertMessage("Successfully Updated Pickup Status!");
          setAlertType("success");
          setAlertOpen(true);
        }
      });

      updatePickup({
        ...pickup, 
        pickup_status: event.target.value
      });
    };
    
    const handleClose = (event, reason) => {
      if (reason === 'clickaway') {
        return;
      }
  
      setAlertOpen(false);
    };

    return (
        <Page
          className={classes.root}
          title="Pick Ups"
        >
          <Container maxWidth={false}>

            <Box mb={3}>
              <Typography variant="h2">
                Manage Pickup
                
              </Typography>
              
              <Typography variant="h3">
                Scheduled Pickup Date: {pickup.scheduled_date}
              </Typography>
              <Typography variant="h3">
                Review Date: {pickup.review_date}
              </Typography>
            </Box>

            <Divider></Divider>

            <Box mb={3} mt={3}>
              <Typography variant="h2">
                Patients Details 
              </Typography>
              <Typography variant="h3">
                <Patient 
                    className={classes.patient} 
                    patient_id={pickup.patient_id}
                />
              </Typography>
            </Box>

            <Divider></Divider>

            <Box mb={3} mt={3}>
              <Typography variant="h2">
                Prescription Details
              </Typography>
              <Typography variant="h2">
                <DrugName 
                  drug_id={pickup.drug_id}
                />
                Drug Quantity: {pickup.drug_quantity}
              </Typography>  
            </Box>
            
            <Divider/>

            <Box mb={3} mt={3}>
              <Typography variant="h2">
                Test Requirements:
              </Typography>
              <Typography variant="h4">
              <PrescriptionTests 
                  pickup_id={id}
                  patient_id={pickup.patient_id}
                />
              </Typography>
              
            </Box>

            <Box mt={3}>
            <Typography variant="h3">
                Status:             
                <FormControl className={classes.formControl}>
                    <Select
                      native
                      value={pickup.pickup_status}
                      onChange={handleChange}
                      inputProps={{
                        name: 'status',
                        id: 'pre-status',
                      }}
                    >
                      <option aria-label="None" value="" />
                      <option value={"AWAITING_PHARMACIST_AUTHORISATION"}>Awaiting Pharmacist Authorisation</option>
                      <option value={"AWAITING_CONFIRMATION"}>Awaiting Confirmation</option>
                      <option value={"AWAITING_ASSEMBLY"}>Awaiting Assembly</option>
                      <option value={"AWAITING_COLLECTION"}>Awaiting Collection</option>
                      <option value={"COLLECTED"}>Collected</option>
                    </Select>
                </FormControl>
              </Typography>
            </Box>


            <Snackbar open={alertOpen} autoHideDuration={2000} onClose={handleClose}>
              <MuiAlert elevation={6} variant="filled" onClose={handleClose} severity={alertType}>
                {alertMessage}
              </MuiAlert>
            </Snackbar>

          </Container>
        </Page>
      );
}

export default PickupView;