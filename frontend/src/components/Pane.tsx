import { ReactNode } from "react";

export default function(props: {
  children: ReactNode,
  className?: string,
}) {
  const className = props.className ? `pane ${props.className}` : "pane";

  return <div className={className}><>{ props.children }</></div>
}
