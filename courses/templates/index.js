/*console.log('Request data...')

setTimeout(() => {
	console.log('Preparing data...')
	setTimeout(() => {
		console.log('Data prepared!')
			}, 2000)
}, 2000)*/

/*const promise = new Promise((resolve, reject) => {
	setTimeout(() => {
		console.log('First');
		resolve('--data--');
	}, 2000)
}).then(x => {
	setTimeout(() => {
		console.log(x)
	}, 2000)	
})

const promise2 = new Promise((resolve, reject) => {
	setTimeout(() => {
		console.log('Second');
		reject('--extra--error--');
	}, 2000)
}).then(x => {
	setTimeout(() => {
		console.log(x)
	}, 2000)	
}).catch(err => alert(err))
*/

let sleep = (ms, url) => {
	return new Promise(resolve => {
		setTimeout(() => resolve(url), ms)
	})
}

Promise.all([sleep(2000, 'youtube.com'), sleep(5000, 'vk.com')]).then(data => console.log(data))
