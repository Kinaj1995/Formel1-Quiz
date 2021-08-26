$(function() {
  $('a#login').on('click', function(e) {
    e.preventDefault()
    $.post('/api/auth/login',
        function(data) {
      //do nothing
    });
    return false;
  });
});

$(function(){  
  $("#logout").on('click', function(e) {
    e.preventDefault()
    $.ajax({
      url:'/api/auth/logout', 
      type:'POST',
      success: function (res){
          document.write(res)
      }
    })

  });
});
