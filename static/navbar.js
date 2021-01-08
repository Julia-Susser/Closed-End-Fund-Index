/*heroku ps:resize web=hobby
Scaling dynos on ⬢ juliasusser-website... done
type  size   qty  cost/mo
────  ─────  ───  ───────
web   Hobby  1    7
(base) FVFX5DU9HV29:website2 jsusser$ heroku certs:auto:enable*/



document.write(
  `

  <div class="header">
    <span><h2>


    Closed End Fund Index - Marina Group</h2></span>

  </div>
<div id="here">
  <div id="navbar">

    <a class="active" href="javascript:void(0)">Home</a>
    <a href="/home">S&P 500</a>
    <a href="/home2">High Yield</a>
    <img src="static/logo.png"></img>

  </div>

  </div>
    `
)

window.onscroll = function() {myFunction()};

var navbar = document.getElementById("navbar");
var img = document.querySelector("img");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    img.style.height = "0px"
    navbar.classList.add("sticky")
    navbar.classList.remove("navbar")
  } else {
    img.style.height = "200px"
    img.style.marginTop = "-150px"
    navbar.classList.add("navbar")
    navbar.classList.remove("sticky");
  }
}
