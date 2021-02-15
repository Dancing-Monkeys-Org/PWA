import React, { useState } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import {
  Box,
  Container,
  Divider,
  makeStyles,
  Typography,
  Select,
  InputLabel
} from '@material-ui/core';
import FormControl from '@material-ui/core/FormControl';
import Page from 'components/Page';
import Patient from '../Patient'
import DrugName from '../DrugName';

const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
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
      updatePickup({
        ...pickup, 
        pickup_status: event.target.value
      });
    };

    return (
        <Page
          className={classes.root}
          title="Pick Ups"
        >
          <Container maxWidth={false}>

            <Box mb={3}>
              <Typography variant="h2">
                Manage Pickup | Pickup ID: {pickup.pickup_id}
                
              </Typography>
              <Typography variant="h3">
                Status: {pickup.pickup_status}
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
                Patient ID: {pickup.patient_id}
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
                {/* <h2>Authorisation Status: {pickup.is_authorised}</h2> */}
            </Box>

            <Divider/>

            <FormControl className={classes.formControl}>
              <InputLabel htmlFor="pre-status">Modify Status</InputLabel>
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
                  <option value={"AWAITING_ASSEMBLY"}>Awaitng Assembly</option>
                  <option value={"AWAITING_COLLECTION"}>Awaiting Collection</option>
                  <option value={"COLLECTED"}>Collected</option>
                </Select>
            </FormControl>

          </Container>
        </Page>
      );
}

export default PickupView;