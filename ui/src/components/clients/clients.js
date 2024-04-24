import React from 'react'

import Row from 'react-bootstrap/Row';
import Col from "react-bootstrap/Col";

import "./client.css"

export default function Clients() {
  return (
    <div className='stat p-3'>
      <Row className=' pb-3'>
        <Col xs="1" />
        <Col xs="6">
          <div className='info-container info-banner p-4'>
            <div style={{paddingRight: "80px"}}>
              <span className='info-text'>
                Ankit Rana
              </span>
              <br />
              <span className='text-sec'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt</span>
              <br />
              <br />
              <button className='btn-alert'><span className='btn-text'>Read more</span></button>
            </div>
          </div>
        </Col>
        <Col xs="4">
          <p className='top text-center text-md-start float-end'>Know more <br /><span className='f-bold'>From Our Clients</span></p>
        </Col>
        <Col xs="1" />
      </Row>
      <Row>
        <Col xs="1" />
        <Col xs="10">
          <div className='d-flex' style={{ overflow: "scroll", justifyContent: "space-between" }}>
            <div className='client'>
              <span>Rajat Garg</span>
            </div>
            <div className='client'>
              <span>Tanya Sharma</span>
            </div>
            <div className='client'>
              <span>Aditi Thakur</span>
            </div>
            <div className='client'>
              <span>Anant Roy</span>
            </div>
          </div>
        </Col>
        <Col xs="1" />
      </Row>
    </div>
  )
}
