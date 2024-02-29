$(document).ready(function () {
  $("table").paging({ limit: 12 });
  $(".sortable").click(function () {
    var column = $(this).attr("data-column");
    var sortOrder = $(this).hasClass("asc") ? -1 : 1;

    // Remove 'asc' and 'desc' classes from all headers
    $(".sortable").removeClass("asc desc");

    // Add appropriate class to indicate sort order
    $(this).toggleClass("asc desc");

    // Sort the table rows based on the selected column
    var rows = $("#inventory-table tbody tr").get();
    rows.sort(function (a, b) {
      var keyA = $(a)
        .find("td." + column)
        .text();
      var keyB = $(b)
        .find("td." + column)
        .text();
      return sortOrder * keyA.localeCompare(keyB);
    });

    // Re-render the table with sorted rows
    $.each(rows, function (index, row) {
      $("#inventory-table tbody").append(row);
    });
  });

  NProgress.start();
  NProgress.done();
  $(".datetimeinput").datepicker({
    changeYear: true,
    changeMonth: true,
    dateFormat: "yy-mm-dd",
  });
});
