import type { MetaFunction } from "@remix-run/node";
import { Link } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    { title: "Read my Mind" },
    { name: "description", content: "Lewis & Clark 2024 spring hackathon" },
  ];
};

export default function Index() {
  const mainStyle = {
    width: "100%",
    height: "100%",
    display: "flex",
    flexDirection: "row" as const,
    alignItems: "space-between",
    justifyContent: "space-between"
  }
  return (
    <div style={mainStyle}>
      <Link to="/newelems">New Thoughts </Link>
      <Link to="/build">Contemplate </Link>
    </div>
  );
}
