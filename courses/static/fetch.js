url = 'https://jsonplaceholder.typicode.com/posts'

function sendRequest(method, url, body = null) {
	const headers = {
		'Content-Type': 'application/json',
	}
	return fetch(url, {
		method : method,
		body: JSON.stringify(body),
		headers: headers,
	}
	).then(response => {
		if (response.ok) {
			return response.json()
		}
		else response.json().then(error => {
			e = new new Error('Что-то не то')
			e.data = error
			throw e
		})
		
	})
}

/*sendRequest('GET', url)
.then(data => console.log(data)).catch(err => console.log(err))
*/

sendRequest('POST', url, {
	name: 'Ivan',
	age: 26,

})
	.then(data => console.log(data))
	.catch(err => console.log(err))