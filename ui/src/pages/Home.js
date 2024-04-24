import React from 'react';

import Blank from "../components/Blank";
import Metrics from '../components/metrics/Metrics';
import Properties from "../components/properties/Properties";
import Info from "../components/info/info";
import Features from "../components/features/features";
import Gallery from '../components/gallery/gallery';
import Clients from '../components/clients/clients';

import Footer from '../components/footer/Footer';

export default function Home() {
  return (
    <div>
        Some Data 
        <Blank />
        <Metrics />
        <Blank />
        <Properties />
        <Blank />
        <Info />
        <Blank />
        <Features />
        <Blank />
        <Gallery />
        <Clients />
        <Blank />
        <Footer />
    </div>
  )
}
