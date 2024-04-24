import React from 'react';

import Col from 'react-bootstrap/Col';

import "./stats.css";
import StatItem from "./StatItem";


export default function Stats() {
  return (
    <>
      <Col xs="6" md>
        <StatItem
          src="images/img_fisrcharthistogram.svg"
          text="5000 +"
          subText="Of real Estate experience"
        />
      </Col>
      <Col xs="6" md>
        <StatItem
          src="images/img_vector.svg"
          text="10 years +"
          subText="Of real Estate experience"
        />
      </Col>
      <Col xs="6" md>
        <StatItem
          src="images/img_fisrmoney.svg"
          text="100 Cr+"
          subText="Of real Estate experience"
        />
      </Col>
      <Col xs="6" md>
        <StatItem
          src="images/img_fisrgem.svg"
          text="800 +"
          subText="Of real Estate experience"
        />
      </Col>
    </>
  )
}
