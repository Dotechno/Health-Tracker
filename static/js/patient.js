$(document).ready(function () {
    $('#patient-table').DataTable();
});

$(document).ready(function () {
    $('#select-patient').selectpicker();
});

function openConfirmModal() {
    $('#myModal').modal('show');
}