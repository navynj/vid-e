const input_tobdb = url => {fetch(url,{
    method: 'POST',
    headers: {
        'Content-Type' : 'application/json'
    },
    body: JSON.stringify({
        'tdb' : document.getElementById('topdb_input').value
    })
})
.then(res => {return res.json()})
.then(data => {console.log(data)})
.catch(error => {console.log(error)}
)};