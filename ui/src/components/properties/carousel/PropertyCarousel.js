import React from 'react';

import Col from 'react-bootstrap/Col';

import "./propertyCarousel.css";
import PropertyItem from "./PropertyItem";


export default function Property() {
  return (
    <>
      <Col xs="6" md>
        <PropertyItem
          src="images/img_fisrcharthistogram.svg"
          text="5000 +"
          subText="Of real Estate experience"
        />
      </Col>
      <Col xs="6" md>
        <PropertyItem
          src="images/img_vector.svg"
          text="10 years +"
          subText="Of real Estate experience"
        />
      </Col>
      <Col xs="6" md>
        <PropertyItem
          src="images/img_fisrmoney.svg"
          text="100 Cr+"
          subText="Of real Estate experience"
        />
      </Col>
    </>
  )
}
