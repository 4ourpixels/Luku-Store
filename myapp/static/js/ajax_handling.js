$(document).ready(function () {
  $("#orderButton").click(function () {
    var selectedSize = $("input[name='size']:checked").val();
    var selectedColor = $("input[name='color']:checked").val();
    if (!selectedSize || !selectedColor) {
      showInlineError("What size and color would you want this in?");
      return;
    }
    var pk = $(this).data("product-id");
    var action = $(this).data("action");
    var orderButton = $(this);
    var cartItemsCount = $("#cartItemsCount");

    $.ajax({
      url: "/handle_order/",
      type: "POST",
      data: {
        pk: pk,
        size: selectedSize,
        color: selectedColor,
        action: action,
        csrfmiddlewaretoken: "{{ csrf_token }}",
      },
      dataType: "json",
      success: function (data) {
        if (data.success) {
          orderButton.text("Already in cart");
          cartItemsCount.text("+1");
          alert("In the bag!");
        } else {
          alert("Error handling order: " + data.error);
        }
      },
      error: function () {
        alert("Failed to make the Ajax request");
      },
    });
  });
  function showInlineError(message) {
    var errorSection = $("#inlineErrorSection");

    if (errorSection.length === 0) {
      errorSection = $(
        "<div id='inlineErrorSection' class='alert alert-danger'></div>"
      );
      $("#yourFormContainer").prepend(errorSection);
    }
    errorSection.text(message);
  }
});
