function setDatatable (table_id, language_url) {
  let table = $(table_id).DataTable({
    "responsive": true,
    "autoWidth": false,
    "language": {
      "url": language_url,
    },
  })
}
