export interface element {
  id: number
  name: string
  order: number|null
}


export const backend_url = "http://localhost:8000/"
export function getRandomElement(setElem: (elem: element) => void) {
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

export function getElement(id: number, setElem: (elem: element) => void) {
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



export function getProduct(parent_left: number, parent_right: number, setElem: (elem: element|null) => void) {
  fetch(backend_url + "operation/fromparents"+ `?parent_left=${parent_left}&parent_right=${parent_right}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
  }).then((response) => {
    if(response.ok) {
      return response.json()
    }
    console.log("error")
    throw new Error("bad response")
  }).then((data) => {
    if (data["child"]) {
      getElement(data.child, setElem)
    }
  }).catch((error) => {
    console.log("setting to null")
    console.log(error)
    setElem(null)
  })
}

export function getAllElements(parent_left: number, parent_right: number, setElems: (elems: element[]) => void) {
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

