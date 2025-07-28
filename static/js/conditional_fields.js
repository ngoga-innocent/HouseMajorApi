// Example: toggle available_number based on feature selection
document.addEventListener("DOMContentLoaded", function () {
  const selects = document.querySelectorAll("select[id$='-feature']");

  selects.forEach(select => {
    select.addEventListener("change", function () {
      const rowId = this.id.split("-")[0];
      const numberField = document.querySelector(`#id_${rowId}-available_number`);
      // TODO: Make AJAX call or preload feature data to determine visibility
    });
  });
});
