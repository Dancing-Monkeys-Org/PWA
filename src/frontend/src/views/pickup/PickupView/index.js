import React, { useState } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import Page from 'components/Page';

const useStyles = makeStyles((theme) => ({
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

    React.useEffect(function effectFunction() {
        fetch('https://dancingmonkeys.tech/api/pickup?pickup_id=' + id.toString(), { 
            headers:  {
                'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTMxNDMyNDcsImV4cCI6MTYxMzIyOTY0NywianRpIjoiZDA0YzRhMmYtMTY3ZC00NzFjLWJlODYtOGJlY2FlZDA1OTBkIiwiaWQiOiIzYzc2YmJlNy0xNTJkLTQ5N2UtYWY4Yi02ZTkzNTMyYmJlZWEiLCJybHMiOiIiLCJyZl9leHAiOjE2MTU3MzUyNDd9.lqxCRYdxSVPEJfXfcb5mMoVm_f29VqsA9xHFyAfOWfY',
                'Accept': '*/*'
            }
            })
            .then(response => response.json())
            .then(data => {
            updatePickup(data);
            });
    }, []);

    return (
        <Page
          className={classes.root}
          title="Pick Ups"
        >
          <Container maxWidth={false}>
            <Box mt={3}>
                <h2>Pickup ID: {pickup.pickup_id}</h2>
                <h2>Patient ID: {pickup.patient_id}</h2>
                <h2>Drug ID:{pickup.drug_id}</h2>
                <h2>Drug Quantity: {pickup.drug_quantity}</h2>
                <h2>Review Date: {pickup.review_date}</h2>
                <h2>Scheduled Date: {pickup.scheduled_date}</h2>
                <h2>Authorisation Status: {pickup.is_authorised}</h2>
                <h2>Pickup Status: {pickup.pickup_status}</h2>
            </Box>
            <Box
              mt={3}
              display="flex"
              justifyContent="center"
            >
            
            </Box>
          </Container>
        </Page>
      );
}

export default PickupView;