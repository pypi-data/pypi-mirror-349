import { Grid2 } from '@mui/material';
import React from 'react';
import GoBackButton from '../components/GoBackButton';

interface IGrafanaPage {
  handleGoBack: () => void;
}
export default function GrafanaPage({ handleGoBack }: IGrafanaPage) {
  return (
    <Grid2 sx={{ display: 'flex', flexDirection: 'column' }}>
      <Grid2 sx={{ display: 'flex' }}>
        <GoBackButton handleClick={handleGoBack} />
      </Grid2>
      <iframe
        src="http://localhost:3000/"
        width="100%"
        height="600"
        style={{ border: 'none' }}
      ></iframe>
    </Grid2>
  );
}
