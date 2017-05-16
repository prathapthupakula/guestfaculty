(function($){ $(document).ready(function(){
    // Start with a filter list showing only its h3 subtitles; clicking on any
    // displays that filter's content; clicking again collapses the list:
    $('#changelist-filter > h3').each(function(){
        var $title = $(this);
        $title.next().toggle();
        $title.css("cursor","pointer");
        $title.click(function(){
            $title.next().slideToggle();
        });
    });

    // Add help after title:
    $('#changelist-filter > h2').append("<span style='font-size: 80%; color: grey;'> (click to hide/unhide)</span>");

    // Make title clickable to hide entire filter:
    var toggle_flag = true;
    $('#changelist-filter > h2').click(function () {
        toggle_flag = ! toggle_flag;
        $('#changelist-filter').find('> h3').each(function(){
                $(this).toggle(toggle_flag);
        });
    });
  });
})(django.jQuery);
