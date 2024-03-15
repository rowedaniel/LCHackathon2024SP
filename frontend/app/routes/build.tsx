import { Builder } from "~/models/builder";
import { Link } from "@remix-run/react";

export default function Build() {
  const mainStyle = {
    width: "100%",
    height: "100%",
    display: "flex",
    flexDirection: "row" as const,
    alignItems: "space-between",
    justifyContent: "space-between"
  }
  return (
    <div>
	  <div style={mainStyle}>
        <Link to="/newelems">New Thoughts </Link>
        <Link to="/">Home </Link>
      </div>
      <Builder />
    </div>
  )
}

