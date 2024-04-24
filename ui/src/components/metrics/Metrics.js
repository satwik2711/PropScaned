import React from 'react';

import Row from 'react-bootstrap/Row';

import Stats from "./stats/Stats";

export default function Metrics() {
    return (
        <div>
            <Row className='text-center m-0'>
                <p className='top'>Our <span className='f-bold'>Metrics</span></p>
            </Row>
            <Row className='stat m-0 px-auto px-md-5'>
                <Stats />
            </Row>
        </div>
    )
}
