  export default async function AccessFetch(url, init_obj) {
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
        if (body.response.errors.hasOwnProperty("email")) {
        throw new Error(body.response.errors.email[0]+". Please register yourself")
       }else{throw new Error(body.response.errors.password[0]+". Please try again")}
    } 
  }