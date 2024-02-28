$(document).ready(function () {
  $("table").paging({ limit: 2 });

  NProgress.start();
  NProgress.done();
  $(".datetimeinput").datepicker({
    changeYear: true,
    changeMonth: true,
    dateFormat: "yy-mm-dd",
  });
});
