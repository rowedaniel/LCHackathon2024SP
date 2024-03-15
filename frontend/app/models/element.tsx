import { useState } from "react"

import { getAllElements } from "~/models/utils"
import type { element } from "~/models/utils"


const elementStyle = {
  borderRadius: "25px",
  border: "2px solid black",
  background: "#6F5060",
  padding: "20px",
  width: "200px",
  height: "120px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  color: "white",
  fontSize: "20px",
}
export function Element({name}: element) {
  return (
    <div style={elementStyle}>
      {name}
    </div>
  )
}
const newElementStyle = {
  width: "100%",
  height: "100%",
  backgroundColor: "transparent",
}
export function NewElement({parent_left, parent_right}: {parent_left: number, parent_right: number}) {
  const [elems, setElems] = useState<element[]|null>(null)
  if(elems === null) {
    getAllElements(parent_left, parent_right, setElems)
    return (
      <div></div>
    );
  }
  return (
    <div style={elementStyle}>
      <label>
        <select name={"child"} style={newElementStyle}>
          {elems.map((elem, i) => (
            <option key={i} value={elem.id.toString()}> {elem.name} </option>
          ))}
        </select>
      </label>
      <button type="submit">Submit</button>
    </div>
  )
}

export function CreateElement() {
  return (
    <div style={elementStyle}>
      <label>
        <input name="name" />
      </label>
      <button type="submit">Submit</button>
    </div>
  )
}

export function Sym({character}: {character: string}) {
  const elementStyle = {
    fontSize: "40px",
    borderRadius: "100%",
    background: "#E7EBC5",
    width: "60px",
    height: "60px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  }
  return (
    <span style={elementStyle}>
      {character}
    </span>
  )
}
