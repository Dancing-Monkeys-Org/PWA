import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import { Pagination } from '@material-ui/lab';
import Page from 'components/Page';
import Toolbar from './Toolbar';
import PickupCard from './PickupCard';

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
  const [pickups, updatePickups] = useState([]);

  const loginVal = JSON.parse(localStorage.getItem("login"));
  const token = loginVal.token;

  React.useEffect(function effectFunction() {
    fetch('https://dancingmonkeys.tech/api/pickups', { 
          headers:  {
            'Authorization': `Bearer ${token}`,
            'Accept': '*/*'
          }
        })
        .then(response => response.json())
        .then(data => {
          updatePickups(data);
        });
  }, []);

  return (
    <Page
      className={classes.root}
      title="Pick Ups"
    >
      <Container maxWidth={false}>
        <Toolbar />
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
        <Box
          mt={3}
          display="flex"
          justifyContent="center"
        >
          <Pagination
            color="primary"
            count={3}
            size="small"
          />
        </Box>
      </Container>
    </Page>
  );
};

export default PickupListView;
