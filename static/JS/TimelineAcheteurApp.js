(function ($) {
    $(function() { // cette ligne est équivalente à $(document).ready(function(){})
       $(".task__detail").each(function () {
           $(this).parent().mouseleave(function () {//quand la souris passe sur l'element
               $(this).children(".task__detail").hide(); // permet de cacher des éléments a l'aide de sélecteur (les mêmes quand css)
           });
           $(this).parent().mouseenter(function () {//quand la souris ressort de l'element
               $(this).children(".task__detail").show();
           });
       });

       $('.task').draggable({
           cursor: 'move',
           containment: 'document',
       });

       $('.item').droppable({
           drop : handleTaskDrop,
           hoverClass: 'hovered',
       });

       function getCookie(name) {
         var cookieValue = null;
         if (document.cookie && document.cookie != '') {
             var cookies = document.cookie.split(';');
             for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                 // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
         }
         return cookieValue;
        }

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        var csrftoken = getCookie('csrftoken');
        // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

       function handleTaskDrop( event, ui ) {

           const draggable = ui.draggable;
           ui.draggable.position({of: $(this), my: 'left top', at: 'left top'});
           const ID = draggable.attr('id');
           const DGA = draggable.css("grid-area");
           const DataDrop = $(this).children().attr('value');
           const DataDrag = draggable.children().first().attr('value')
           console.log(DataDrag)
           const GC = $(this).css("grid-column");
           const jsonString = 'DataDrop=' + DataDrop + '&DataDrag=' + DataDrag + "&GC=" + GC + "&ID=" + ID + "&DGA=" + DGA;

           $.ajax({
               type: "POST",
               data: jsonString,
               dataType : "html",
               url: "../../../../RefreshTimelineAchat/"
           });
           setTimeout(function(){ location.reload(true); }, 100);

       }

    });

})(jQuery);