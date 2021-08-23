let anwsered = false
let qcorrect = false
$(function() {
    $('.c').on('click', function(e) {
      e.preventDefault()
      $(this).toggleClass("correct")
      anwsered = true
      qcorrect = true
      console.log(qcorrect)
      lookbtn()
      return false;
    });
});
  
$(function() {
    $('.w').on('click', function(e) {
        e.preventDefault()
        $(this).toggleClass("wrong")
        anwsered = true
        lookbtn()
        return false;
    });
});


function lookbtn(){
    
    $('.optbtn').prop('disabled', true);
}

$("#quiz").submit(function(e) {
    e.preventDefault();
});

$(function() {
    var segment_str = window.location.pathname;
    var segment_array = segment_str.split( '/' );
    var last_segment = segment_array.pop();

    $('#next').on('click', function(e) {
        var form = $('#quiz')
        
        $.ajax({
            url:'next/', 
            type:'POST',
            contentType: 'application/json',
            data: JSON.stringify({'Correct': qcorrect, 'Diff_id': last_segment}),
            success: function (res){
                document.write(res)
            }
        })
    });
});
