// alert('Hello')
var socket = io.connect('http://localhost:5000')

socket.on('connect', function () {
  socket.emit('myevent', { message: 'I am now connected!' })
})
