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
