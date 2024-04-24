import React from 'react'

export default function StatItem({ src, text, subText }) {
  return (
    <div className='stat-container'>
      <img
        className='stat-img'
        src={src}
        alt="svg"
      />
      <div>
        <span
          className="stat-text"
        >
          {text}
        </span>
        <br />
        <span
          className="subtext"
        >
          {subText}
        </span>
      </div>
    </div>
  )
}
