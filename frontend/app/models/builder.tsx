import { useState, useEffect, SyntheticEvent } from "react"

import { Element, NewElement, Sym } from "~/models/element"
import { backend_url, getRandomElement, getProduct } from "~/models/utils"
import type { element } from "~/models/utils"


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
    getRandomElement((newLeft) => {
      getRandomElement((newRight) => {
        setLeft(newLeft)
        setRight(newRight)
        getProduct(newLeft.id, newRight.id, setChild)
      })
    })
  }, [setLeft, setRight, setChild])

  if(!left || !right) {
      return (
        <form method="post" onSubmit={handleNewElement}>
          <div style={builderStyle}>
            <Element id={0} name={""} order={0} />
            <Sym character={"+"} />
            <Element id={0} name={""} order={0} />
            <Sym character={"="} />
            <Element id={0} name={""} order={0} />
          </div>
        </form>
	)
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
    .then((response) => { 
        console.log(response.json())
        getRandomElement((newRight) => {
          getProduct(left.id, newRight.id, setChild)
          setRight(newRight)
        })
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
