const observable = Rx.Observable.create(observer=>{
	observer.next("hello");
	observer.next("world");
})

const clicks = Rx.Observable.fromEvent(document,"click")

const interval = Rx.Observable.interval(500);

const anything = Rx.Observable.of("hello",["hi","hey","welcome"],23);

function print(val){
	let el = document.createElement('p')
	el.innerText = val
	document.body.appendChild(el)
}

observable.subscribe(val=>print(val))
clicks.subscribe(val=>console.log(val))

const subscription = interval.subscribe(int=>print(new Date().getSeconds()))
setTimeout(()=>{
	subscription.unsubscribe()
},3000)


anything.subscribe(val=>console.log(val))

const numbers = Rx.Observable.of(10,20,30)
numbers.map(x=>Math.log(x)).subscribe(val=>console.log(val))
const jsonString = '{"type":"dog", "race":"dalmatien"}'
const transform = Rx.Observable.of(jsonString);

transform.map(jsonS=>JSON.parse(jsonS)).subscribe(obj=>console.log(obj.type))

numbers.filter(n=>n>10).subscribe(n=>console.log(n))

const stringUrl = Rx.Observable.of("university/departement/1/","university/departement/2/","university/professor/Famaey/")

stringUrl
	.startWith("university/professor/Famaey")
	.scan((acc, cur) => [acc[1], cur], ["/", "/"])
	.map(acc => acc[0])
  	.subscribe(console.log)

//clicks.map(e=> parseInt(Math.random()*10)).do(n=>print("score"+ ${n})).scan((highscore,score)=>highscore+score).subscribe(highscore=>print("highscore"+${highscore}))
