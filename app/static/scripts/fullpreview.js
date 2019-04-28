$(document).ready(function() {
  $(".view").click(function () {
    $(".modal").removeClass("hidden");
    });
    $(".modal").click(function() {
      $(".modal").addClass("hidden");
    });
});
