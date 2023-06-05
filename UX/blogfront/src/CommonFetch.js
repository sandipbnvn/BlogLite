export default async function CommonFetch(url, init_obj) {
    let resp = null
    let body = null
    try {
        resp = await fetch(url, init_obj)
    } catch {
      throw new Error('Network connection failed')
    }
    try {
        body = await resp.json()
    } catch {
      throw new Error('Response body was not json')
    }
  
    if (resp.ok) {
      return body
    } else {
      alert(body.message)
      throw new Error(body.message)
    }
  }

//   export default async function AccessFetch(url, init_obj) {
//     let resp = null
//     let body = null
//     try {
//         resp = await fetch(url, init_obj)
//     } catch {
//         throw new Error('Network connection failed')
//     }
//     try {
//         body = await resp.json()
//     } catch {
//         throw new Error('Response body was not json')
//     }
     
//     if (resp.ok) {
//         return body
//     } else {
//         throw new Error(body.response)
//     }
//     }