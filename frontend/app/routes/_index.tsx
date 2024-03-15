import type { MetaFunction } from "@remix-run/node";

import { Builder } from "~/models/builder";

export const meta: MetaFunction = () => {
  return [
    { title: "Read my Mind" },
    { name: "description", content: "Lewis & Clark 2024 spring hackathon" },
  ];
};

export default function Index() {
  return (
    <div>
      <Builder />
    </div>
  );
}
