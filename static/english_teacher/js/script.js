document.addEventListener('DOMContentLoaded', () => {  

    window.onscroll = function() {scrollFunction()};

    function scrollFunction() {
      if (document.body.scrollTop > 1 || document.documentElement.scrollTop > 1) {
        document.getElementById("navbar").classList.add('fader');
        document.getElementById("navbar").classList.remove('fade_start')
      } else {
        document.getElementById("navbar").classList.add('fade_start');
        document.getElementById("navbar").classList.remove('fader');
      }
      document.getElementById("navbar").addEventListener('mouseover', () => {
        document.getElementById("navbar").classList.add('fade_start');
        document.getElementById("navbar").classList.remove('fader');
      })
    }
    function mouseNav() {
        document.getElementById("navbar").addEventListener('click', () => {
            document.getElementById("navbar").classList.remove('fade_start')
            document.getElementById("navbar").classList.add('fader');
        })
    }  
});