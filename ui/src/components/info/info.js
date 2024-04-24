import React from 'react'

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import "./info.css"

export default function Info() {
    return (
        <div>
            <Row className='m-0'>
                <Col md="1"></Col>
                <Col md="3">
                    <div>
                        <p className='top text-center text-md-start'>Why <span className='f-bold'>Propscan?</span></p>
                        <p className='subtext' style={{ textAlign: "left" }}>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ipsum orci, tincidunt et aliquam eget, pharetra id sapien. Sed dapibus ut enim eget viverra. Nam aliquet odio nulla, vitae imperdiet velit vestibulum id. Cras et turpis sed velit auctor euismod et id felis. Aenean elementum ligula metus, ac bibendum dolor fringilla eget. Mauris nisi eros, semper sit amet posuere id, imperdiet vitae est. Sed tincidunt mi eget efficitur sagittis. Maecenas fermentum turpis tellus, in laoreet orci ullamcorper vel.</p>
                    </div>
                </Col>
                <Col md="1"></Col>
                <Col>
                    <div className='info-container info-banner'>
                        <div>
                            <span className='info-text'>
                                Aapki Apni
                            </span>
                            <br />
                            <span className='info-text info-subtext' >
                                Application
                            </span>
                            <br/>
                            <br/>
                            <button className='btn-alert'><span className='btn-text'>Button Sample</span></button>
                        </div>
                        <img
                            className='info-img'
                            src="images/img_image28.png"
                            alt="svg"
                        />
                    </div>
                </Col>
                <Col md="1"></Col>
            </Row>
        </div>
    )
}

