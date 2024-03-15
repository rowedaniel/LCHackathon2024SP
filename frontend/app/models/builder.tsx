import { useState, FormEventHandler, SyntheticEvent } from "react"


interface element {
  id: number
  name: string
}

// Current color palette:
// 989788
// 51344D
// 6F5060
// A78682
// E7EBC5
const builderStyle = {
  display: "flex",
  flexDirection: "row" as const,
  justifyContent: "space-between",
  alignItems: "center",
}
export function Builder() {
  const [left, setLeft] = useState<element>()
  const [right, setRight] = useState<element>()

  // TODO: currently, this re-renders the elements several times before settling in.
  // Consider using fancier react stuff (effects maybe?) to stop this
  if(!left) {
    getRandomElement(setLeft)
    return (
      <div></div>
    );
  }
  if(!right) {
    getRandomElement(setRight)
    return (
      <div></div>
    );
  }

  function handleNewElement(event: SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    console.log(formData)
    console.log([...formData.entries()]);
  }

  return (
    <form method="post" onSubmit={handleNewElement}>
      <div style={builderStyle}>
        <Element {...left} />
        <Sym character={"+"} />
        <Element {...right} />
        <Sym character={"="} />
        <NewElement parent_left={left.id} parent_right={right.id} />
      </div>
    </form>
  )
}

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
function Element({name}: element) {
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
function NewElement({parent_left, parent_right}: {parent_left: number, parent_right: number}) {
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
        <select name={"parent_left"} defaultValue={parent_left} style={{display: "none"}}></select>
        <select name={"parent_right"} defaultValue={parent_right} style={{display: "none"}}></select>
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

function Sym({character}: {character: string}) {
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

const backend_url = "http://localhost:8000/"
function getRandomElement(setElem: (elem: element) => void) {
  fetch(backend_url + "element/random", {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    if(response.ok) {
      return response.json()
    } else {
      return {name: "not found"}
    }
  }).then((data) => {
    setElem(data)
  })
}

function getElement(id: number, setElem: (elem: element) => void) {
  fetch(backend_url + "element/id" + `?item_id=${id}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    if(response.ok) {
      return response.json()
    } else {
      return {name: "not found"}
    }
  }).then((data) => {
    setElem(data)
  })
}



function getProduct(parent_left: number, parent_right: number, setElem: (elem: element) => void) {
  fetch(backend_url + "operation/fromparents"+ `?parent_left=${parent_left}&parent_right=${parent_right}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    if(response.ok) {
      return response.json()
    } else {
      return []
    }
  }).then((data) => {
    getElement(data.child, setElem)
  })
}

function getAllElements(parent_left: number, parent_right: number, setElems: (elems: element[]) => void) {
  fetch(backend_url + "element/allpossible"+ `?parent_left=${parent_left}&parent_right=${parent_right}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    if(response.ok) {
      return response.json()
    } else {
      return []
    }
  }).then((data) => {
    setElems(data)
  })
}

