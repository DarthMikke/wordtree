import React, { ReactNode, useState } from "react"

function Dropdown ({title, children, type, }: {
  title: string | undefined,
  children?: ReactNode,
  type?: string,
}) {
  const [isOpen, setOpen] = useState<Boolean>(false);

  return <button
   className={`button ${type} dropdown-toggle ${isOpen ? "open" : ""}`}
   onClick={() => { setOpen(!isOpen) } } aria-label={ "open submenu" }>
    { title && title }
    { <ul className={`dropdown__list`}>{ React.Children.toArray(children).map((x) => <li className="dropdown__item">{x}</li>) }</ul> }
  </button>
}

export default Dropdown;
