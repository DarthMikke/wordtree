import * as Plot from "@observablehq/plot";
import { LegacyRef, useEffect, useRef } from "react";

/**
 * @see https://codesandbox.io/s/plot-react-csr-p4cr7t
 */
export default function PlotFigure({options}: {options: object}) {
  const containerRef = useRef<HTMLElement>();

  useEffect(() => {
    if (options == null) return;
    const plot = Plot.plot(options);
    containerRef!.current!.append(plot);
    return () => plot.remove();
  }, [options]);

  return <div className="main_plot" ref={containerRef as LegacyRef<HTMLDivElement>} />;
}
