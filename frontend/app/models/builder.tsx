import { useState, useEffect, SyntheticEvent } from "react"


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
  const [child, setChild] = useState<element|null>()

  useEffect(() => {
    getRandomElement(setLeft)
    getRandomElement(setRight)
  }, [setLeft, setRight])
  useEffect(() => {
    if(!left || !right) return
    getProduct(left.id, right.id, setChild)
  }, [left, right, setChild])

  if(!left || !right) {
      return
  }


  function handleNewElement(event: SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    const formProps = Object.fromEntries(formData);
    const child = formProps.child
    if(!left || !right) {
        return
    }

    fetch(backend_url + "operation/create", {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },

      //make sure to serialize your JSON body
      body: JSON.stringify({
        parent_left: left.id,
        parent_right: right.id,
        child: child
      })
    })
    .then( (response) => { 
       console.log(response)
        getRandomElement(setRight)
    });

  }

  if(!child) {
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
  } else if(child) {
      return (
        <form method="post" onSubmit={handleNewElement}>
          <div style={builderStyle}>
            <Element {...left} />
            <Sym character={"+"} />
            <Element {...right} />
            <Sym character={"="} />
            <Element {...child} />
          </div>
        </form>
      )
  }
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
    }
    throw new Error("bad response")
  }).then((data) => {
    setElem(data)
  }).catch((error) => {
    console.log(error)
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
    }
    throw new Error("bad response")
  }).then((data) => {
    setElem(data)
  }).catch((error) => {
    console.log(error)
  })
}



function getProduct(parent_left: number, parent_right: number, setElem: (elem: element|null) => void) {
  fetch(backend_url + "operation/fromparents"+ `?parent_left=${parent_left}&parent_right=${parent_right}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    console.log(response)
    if(response.ok) {
      return response.json()
    }
    throw new Error("bad response")
  }).then((data) => {
    if (data["child"]) {
      getElement(data.child, setElem)
    }
  }).catch((error) => {
    console.log("setting to null")
    setElem(null)
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
    }
    throw new Error("bad response")
  }).then((data) => {
    setElems(data)
  }).catch((error) => {
    console.log(error)
  })
}

