$(document).ready(function() {
  $(".edit").click(function () {
    console.log("clicked box");
    $(".clickedit").addClass("editing");
    $(".clickedit").attr("contenteditable", true);
    console.log("clickedit");
    $(".edit").attr("src", "../static/images/checkicon.png");
    $(".edit").click(function () {
        console.log("clicked box");
        $(".clickedit").removeClass("editing");
        $(".clickedit").attr("contenteditable", false);
        console.log("clickedit");
        $(".edit").attr("src", "../static/images/editicon.png");
      });
    });
});
