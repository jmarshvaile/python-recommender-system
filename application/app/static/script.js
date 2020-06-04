$(document).ready(function(){
    $('#selectedTags').on('shown.bs.collapse', function() {
        $("#selectedCaret").addClass('fa-caret-left').removeClass('fa-caret-right');
    });
    $('#selectedTags').on('hidden.bs.collapse', function() {
        $("#selectedCaret").addClass('fa-caret-right').removeClass('fa-caret-left');
    });
    
    $('#recommendedTags').on('shown.bs.collapse', function() {
        $("#recommendedCaret").addClass('fa-caret-left').removeClass('fa-caret-right');
    });
    $('#recommendedTags').on('hidden.bs.collapse', function() {
        $("#recommendedCaret").addClass('fa-caret-right').removeClass('fa-caret-left');
    });
})