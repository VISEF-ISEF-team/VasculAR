var i = 0
function move() {
  if (i == 0) {
    i = 1
    var elem = document.getElementById('myBar')

    var width = 10
    var id = setInterval(frame, 400)
    function frame() {
      if (width >= 100) {
        clearInterval(id)
        i = 0
      } else {
        width++
        elem.style.width = width + '%'
        elem.innerHTML = width + '%'
      }
    }
  }
}
function move2() {
  if (i == 0) {
    i = 1
    var elem = document.getElementById('myBar2')


    var width = 10
    var id = setInterval(frame, 500)
    function frame() {
      if (width >= 100) {
        clearInterval(id)
        i = 0
      } else {
        width++
        elem.style.width = width + '%'
        elem.innerHTML = width + '%'
      }
    }
  }
}