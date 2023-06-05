  export default async function RegisterFetch(url, init_obj) {
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
        return "Registered Successfully, Please Login"
    } else {
        throw new Error("email already registered. Please Login")
       }
  }