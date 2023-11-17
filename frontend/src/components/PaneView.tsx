export default function(props: {
  children: object[] | object,
}) {
  return <div className="panes"><>{ props.children }</></div>
}
