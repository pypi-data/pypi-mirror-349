import { Paper } from '@mui/material';
import React from 'react';

// import BandHighLight from '../components/BandHighLight';
// import ElementHighlights from '../components/ElementHighlights';
// import MapComponent from '../components/map/MapComponent';

/**
 * This is something temporary. Just for the demo on April 8th, on All-Hands Meeting for GreenDIGIT.
 */
const chartLinks = [
  // CPU Usage: used and total
  'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=2&__feature.dashboardSceneSolo',
  // Memory used
  'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=3&__feature.dashboardSceneSolo',
  // Network received/sent
  'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743669689152&to=1743691289152&timezone=browser&theme=light&panelId=4&__feature.dashboardSceneSolo',
  // Thread Nr.
  'http://localhost:3000/d-solo/behmsglt2r08wa/2025-04-08-demo?orgId=1&from=1743670340144&to=1743691940144&timezone=browser&theme=light&panelId=5&__feature.dashboardSceneSolo'
];

const styles: Record<string, React.CSSProperties> = {
  main: {
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    height: '100%',
    flexWrap: 'wrap',
    boxSizing: 'border-box',
    padding: '10px',
    whiteSpace: 'nowrap'
  },
  grid: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
    // flex: '0 1 50%'
    // width: '50%'
    // border: '1px solid green',
    // boxSizing: 'border-box',
  }
};

interface ITempIframe {
  keyIndex: number;
  url: string;
}

function TempIframe({ keyIndex, url }: ITempIframe) {
  return (
    <iframe
      src={url}
      width="100%"
      height="400px"
      sandbox="allow-scripts allow-same-origin"
      // ref={iframeRef}
      id={`iframe-item-${keyIndex}`}
      style={{ border: 'none', margin: '5px' }}
    />
  );
}

export default function GeneralDashboard() {
  function GridContent({ index }: { index: number }) {
    return <TempIframe keyIndex={index} url={chartLinks[index]} />;
    // switch (index) {
    //   case 1:
    //     return <TempIframe keyIndex={1} />;
    //   case 2:
    //     return <TempIframe keyIndex={2} />;
    //   case 3:
    //     return <MapComponent />;
    //   default:
    //     return <span>{'Grid element ' + String(index)}</span>;
    // }
  }

  const gridElements = Array.from(new Array(chartLinks.length));

  return (
    <div style={styles.main}>
      {gridElements.map((value: number, index: number) => {
        return (
          <Paper
            key={`grid-element-${value}`}
            style={{
              ...styles.grid
              // minWidth: value === 3 ? '100%' : '50%',
              // flex: value === 3 ? '0 1 100%' : '0 1 50%'
            }}
          >
            <GridContent index={index} />
          </Paper>
        );
      })}
    </div>
  );
}
