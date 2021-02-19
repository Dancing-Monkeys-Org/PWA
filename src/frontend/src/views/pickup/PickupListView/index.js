import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Select,
  Typography,
  makeStyles
} from '@material-ui/core';
import Page from 'components/Page';
import Toolbar from './Toolbar';
import PickupCard from './PickupCard';
import FormControl from '@material-ui/core/FormControl';
import DatePicker from "react-datepicker";
import moment from 'moment';

import "react-datepicker/dist/react-datepicker.css";

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

const PickupListView = () => {
  const classes = useStyles();
  const [filter, setFilter ] = useState({ date: new Date(), status: "AWAITING_PHARMACIST_AUTHORISATION" });
  const [pickups, updatePickups] = useState([]);

  const loginVal = JSON.parse(localStorage.getItem("login"));
  const token = loginVal.token;

  React.useEffect(function effectFunction() {
    fetch('https://dancingmonkeys.tech/api/pickups?scheduled_before=' + moment(filter.date).format('YYYY-MM-DD') + '&pickup_status=' + filter.status, { 
          headers:  {
            'Authorization': `Bearer ${token}`,
            'Accept': '*/*'
          }
        })
        .then(response => response.json())
        .then(data => {
          updatePickups(data);
        });
  }, [filter]);

  const handleChange = (event) => { 
    setFilter({...filter, status: event.target.value});
  }

  return (
    <Page
      className={classes.root}
      title="Pick Ups"
    >
      <Container maxWidth={false}>
        <Box mt={3}>
          <Typography variant="h4">
            Scheduled Date:
            <DatePicker selected={filter.date} onChange={date => setFilter({...filter, date: date})} />
          </Typography>
            <Typography variant="h4">
                Status:             
                <FormControl className={classes.formControl}>
                    <Select
                      native
                      value={filter.status}
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
        <Box mt={3}>
          <Grid
            container
            spacing={3}
          >
            {pickups.map((pickup) => (
              <Grid
                item
                key={pickup.pickup_id}
                lg={4}
                md={6}
                xs={12}
              >
                <PickupCard
                  className={classes.pickupCard}
                  pickup={pickup}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Page>
  );
};

export default PickupListView;
