import React from 'react'

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import "./gallery.css"

export default function Gallery() {
    return (
        <Row>
            <Col xs="1" />
            <Col xs="10">

        <div className='px-2'>
            <p className='top text-center text-md-start'>Aapki <span className='f-bold'>Gallery</span></p>
            <div>
                <span style={{
                    fontFamily: "Poppins",
                    fontStyle: "normal",
                    fontWeight: "400",
                    fontSize: "16px",
                    lineHeight: "22px",
                    color: "#4F4F4F",
                }}>Have a look on the Top localities
                </span>
                <button className='btn-info' style={{ float: "right" }}><span className='btn-text'>View More</span></button>
            </div>
            <div className='my-5'>
                <Row className='m-0 p-0'>
                    <Col className='p-0'>
                    <div className='d-flex' style={{overflow: "scroll", justifyContent:"space-between"}}>
                        <div className='p-0'>
                            <img
                                src="images/img_rectangle41.png"
                                width="246px"
                                height="246px"
                            />
                            <br />
                            <span className='city'>Dwarka</span>
                        </div>
                        <div className='p-0'>
                            <img
                                src="images/img_rectangle42.png"
                                width="246px"
                                height="246px"
                            />
                            <br />
                            <span className='city'>Saket</span>
                        </div>
                        <div className='p-0'>
                            <img
                                src="images/img_rectangle43.png"
                                width="246px"
                                height="246px"
                            />
                            <br />
                            <span className='city'>Janakpuri</span>
                        </div>
                        <div className='p-0'>
                            <img
                                src="images/img_rectangle44.png"
                                width="246px"
                                height="246px"
                            />
                            <br />
                            <span className='city'>Uttam Nagar</span>
                        </div>
                    </div>
                    </Col>
                </Row>
            </div>
        </div>
            </Col>
            <Col xs="1" />
        </Row>
    )
}
