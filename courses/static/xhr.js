url = 'http://127.0.0.1:8000/course/json/'

function sendRequest(method, url, body = null) {
	return new Promise((resolve, reject) => {
		xhr = new XMLHttpRequest()
		xhr.open(method, url)
		/*xhr.responseType = 'json'*/
		xhr.setRequestHeader('Content-Type', 'application/json')
		xhr.send(body)
		xhr.onerror = () => reject('--error--')
		xhr.onload = () => resolve(JSON.parse(xhr.response))
	})
	
}

let getFunc = () => {
	sendRequest('GET', url).then(data => console.log(data)).catch(err => console.log(err))
}

body = {
		"model": "courses.course",
		"pk": 11,
		"fields": {
			"name": "COURSE EXTRA",
			"slug": "course-extra",
			"subject": 2,
			"owner": 1,
			"created": "2021-10-06",
			"overview": "EXTRA, eng",
			"price": 1500,
			"views_count": 14,
			"mean_rating": "5.00",
			"students": [1, 2]
					}
	}

let postFunc = () => {
	sendRequest('post', url, body).then(data => console.log(data)).catch(err => console.log(err))
}



let getButt = document.querySelector('button.get')
let postButt = document.querySelector('button.post')

getButt.addEventListener('click', () => {
	getFunc()
})

postButt.addEventListener('click', () => {
	postFunc()
})

/*
let text = document.querySelector('input.test')
console.log(text)
text.addEventListener('dblclick', () => {
	alert("DON'T CLICK ON IT TWICE")
})
*/



