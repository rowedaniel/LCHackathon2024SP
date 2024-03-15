import {  SyntheticEvent } from "react"
import { Link } from "@remix-run/react";
import { CreateElement } from "~/models/element"
import { backend_url } from "~/models/utils"

export default function NewElems() {
  function handleCreateElement(event: SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    const formProps = Object.fromEntries(formData);

    fetch(backend_url + "operation/create", {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },

      //make sure to serialize your JSON body
      body: JSON.stringify({
        name: formProps.name,
        order: null
      })
    })
    .then((response) => { 
        console.log(response.json())
    });

  }
  const mainStyle = {
    width: "100%",
    height: "100%",
    display: "flex",
    flexDirection: "row" as const,
    alignItems: "space-between",
    justifyContent: "space-between"
  }
  return (
    <form method="post" onSubmit={handleCreateElement}>
      <div style={mainStyle}>
        <Link to="/">Home </Link>
        <Link to="/build">Contemplate </Link>
      </div>
	  <div>
        <CreateElement />
      </div>
    </form>
    )
}

