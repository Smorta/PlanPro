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
           stop: dragEnd,
           start : dragStart
       });

       function dragStart(event,ui) {
       }

       function dragEnd(event,ui) {
       }

       $('.item').droppable({
           drop : handleTaskDrop,
           hoverClass: 'hovered',
       });

       function handleTaskDrop( event, ui ) {
           var draggable = ui.draggable;
           ui.draggable.position({of: $(this), my: 'left top', at: 'left top'});
           var GR = $(this).css("grid-row");
           var GC = $(this).css("grid-column")
           var jsonString = JSON.stringify({grid_row: GR, grid_column: GC});
           console.log(jsonString);

           $.ajax({
               type: "GET",
               data: jsonString,
               url: "../../../../RefreshTimelineChant/"
           });
       }

   });

})(jQuery);
// travaiiller avec deux variables

