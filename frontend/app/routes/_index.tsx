import type { MetaFunction } from "@remix-run/node";
import React, { useState } from "react";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  const [firstName, setFirstName] = useState('');
  
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: "1.8" }}>
	  <h>progress:</h>
      <input value = {firstName} onChange={e=> setFirstName(e.target.value)} />
	  <p>{firstName}</p>
    </div>
  );
}
