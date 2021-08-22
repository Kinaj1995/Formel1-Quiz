let anwsered = false
let correct = false
$(function() {
    $('.c').on('click', function(e) {
      e.preventDefault()
      $(this).toggleClass("correct")
      this.anwsered = true
      this.correct = true
      lookbtn()
      return false;
    });
});
  
$(function() {
    $('.w').on('click', function(e) {
        e.preventDefault()
        $(this).toggleClass("wrong")
        this.anwsered = true
        lookbtn()
        return false;
    });
});


function lookbtn(){
    
    $('.optbtn').prop('disabled', true);
}
