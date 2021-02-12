import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import {
  Avatar,
  Box,
  Card,
  CardContent,
  Divider,
  Grid,
  Typography,
  makeStyles
} from '@material-ui/core';
import { Link } from 'react-router-dom'
import DrugName from '../DrugName'
import AccessTimeIcon from '@material-ui/icons/AccessTime';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column'
  },
  statsItem: {
    alignItems: 'center',
    display: 'flex'
  },
  statsIcon: {
    marginRight: theme.spacing(1)
  }
}));

const PickupCard = ({ className, pickup, ...rest }) => {
  const classes = useStyles();

  return (
    <Link to={'/app/pickup/' + pickup.pickup_id}>
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardContent>

      <Typography
          align="left"
          color="textPrimary"
          gutterBottom
          variant="h4"
        >
          <DrugName
                className={classes.drugName}
                drug_id={pickup.drug_id}
          /> 
        </Typography>

        <Typography
          align="left"
          color="textPrimary"
          gutterBottom
          variant="h4"
        >
          Quantity: {pickup.drug_quantity} 
        </Typography>

        <Typography
          align="left"
          color="textPrimary"
          gutterBottom
          variant="h4"
        >
          {/* Patient: {pickup.patient.patient_name} */}
        </Typography>

        <Typography
          align="left"
          color="textPrimary"
          variant="h4"
        >
          Status: {pickup.pickup_status}
        </Typography>

      </CardContent>

      <Box flexGrow={1} />
      <Divider />
      <Box p={2}>
        <Grid
          container
          justify="space-between"
          spacing={2}
        >
          <Grid
            className={classes.statsItem}
            item
          >
            <AccessTimeIcon
              className={classes.statsIcon}
              color="action"
            />
            <Typography
              color="textSecondary"
              display="inline"
              variant="body2"
            >
              Scheduled {pickup.scheduled_date} | Review Date {pickup.review_date}
            </Typography>
          </Grid>
        </Grid>
      </Box>
      
    </Card>
    </Link>
  );
};

PickupCard.propTypes = {
  className: PropTypes.string,
  pickup: PropTypes.object.isRequired
};

export default PickupCard;
