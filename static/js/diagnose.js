/* Diagnosis search functionality */

$(document).ready(function () {
  $(".recipes").select2({
    placeholder: "Search for...",
    allowClear: true,
    tags: true,
    tokenSeparators: [",", " "],
    /*ajax: {
        url: '/example/api',
        delay: 500
      }*/
  });
});
