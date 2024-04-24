import React from 'react'

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import "./footer.css"

export default function Footer() {
  return (
    <div style={{
      backgroundColor: "#092C4C",
      padding: "48px 128px"
    }}>
      <Row style={{ color: "#FFFFFF" }}>
        <Col xs="6" md="3" className='my-2'>
          <p className='heading'>COMPANY</p>
          <div className='items'>
            <p className='mb-2'>Careers</p>
            <p className='mb-2'>About Us</p>
            <p className='mb-2'>For Partners</p>
            <p className='mb-2'>Terms</p>
            <p className='mb-2'>Annual Returns</p>
            <p className='mb-2'>Privacy Policy</p>
            <p className='mb-2'>Contact Us</p>
            <p className='mb-2'>Unsubscribe</p>
            <p className='mb-2'>Merger Hearing Advertisement</p>
          </div>
        </Col>
        <Col xs="6" md="3" className='my-2'>
          <p className='heading'>Explore</p>
          <div className='items'>
            <p className='mb-2'>News</p>
            <p className='mb-2'>Home Loans</p>
            <p className='mb-2'>Sitemap</p>
            <p className='mb-2'>Rent Contracts</p>
            <p className='mb-2'>International</p>
          </div>
        </Col>
        <Col xs="6" md="3" className='my-2'>
          <p className='heading'>Services</p>
          <div className='items'>
            <p className='mb-2'>Buy</p>
            <p className='mb-2'>Sell</p>
            <p className='mb-2'>Rent</p>
            <p className='mb-2'>Co-Living</p>
            <p className='mb-2'>Plots Buy</p>
            <p className='mb-2'>And Many More</p>
          </div>
        </Col>
        <Col xs="6" md="3" className='my-2'>
          <p className='heading'>Open Camera & Scan the QR</p>
          <div className='items'>
          <img 
          src="images/img_image30.png"
          style={{
            width:"11vw",
            height:"11vw",
            objectFit:"cover",
            marginTop:"20px",
            display:"block",
            marginRight:"auto"
          }}
        />
          </div>
        </Col>
      <Col>
      <div className='tag-line'>
        <img 
          src="images/check.svg"
          style={{
            width:"24px",
            height:"24px",
            marginRight:"10px"
          }}
        />
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ipsum orci, tincidunt et aliquam eget, pharetra id sapien. Sed dapibus ut enim eget viverra. Nam aliquet odio nulla, vitae imperdiet velit vestibulum id. Cras et turpis sed velit auctor euismod et id felis.
      </div>
      </Col>
      </Row>
    </div>
  )
}
