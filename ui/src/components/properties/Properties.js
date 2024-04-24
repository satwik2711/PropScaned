import React from 'react';

import Row from 'react-bootstrap/Row';

import PropertyCarousel from "./carousel/PropertyCarousel";

export default function Properties() {
    return (
        <div>
            <Row className='text-center m-0'>
                <p className='top'><span className='f-bold'>Properties</span> for Sale</p>
            </Row>
            <Row className='stat m-0'>
                <PropertyCarousel />
            </Row>
        </div>
    )
}
