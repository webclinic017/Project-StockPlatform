import React from "react"

const FilterLayout = ({ children, title }) => {
  return (
    <div className="filter-layout">
      <div className="filter-layout-title">{title}</div>
      <div className="filter-layout-contents">{children}</div>
    </div>
  )
}

export default FilterLayout
