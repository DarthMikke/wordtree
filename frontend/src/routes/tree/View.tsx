import * as Plot from "@observablehq/plot";
import { stratify, hierarchy } from "d3-hierarchy";
import { useEffect, useState } from "react";
import { useLoaderData } from "react-router";
import Pane from "../../components/Pane";
// import Dropdown from "../../components/Dropdown";
import PlotFigure from "../../Plot";

type Word = {
  "id": number,
  "word": string,
  "language": string,
  "parent": number
}

export default function() {
  const data = useLoaderData() as ({ data: Word[] } | null);
  const [stratified, setStratified] = useState({});

  useEffect(() => {
    if (!data || !(data as unknown as {data: Word[]}).data) return;
    setStratified(
      stratify()
        .id(d => (d as Word).id.toString())
        .parentId(d => ((d as Word).parent as unknown as string))
        (data.data)
    );
  }, [data]);

  return <Pane>
    <PlotFigure options={{
          axis: null,
          marks: [
            Plot.tree(
              hierarchy(stratified).leaves(),
              {
                path: (node) => {
                  console.debug(
                    node.data.data,
                    node.ancestors().reverse()
                    // .map((n: { data: {data: Word} }) => n.data)
                  )
                  return node.ancestors().reverse()
                    .map((n: { data: Word }) => n.data.word).join("|")
                },
                // delimiter: "|",
              }
            )
          ]
        }}/>
  </Pane>
}
