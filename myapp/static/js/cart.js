var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var photoId = this.dataset.product;
    var action = this.dataset.action;
    console.log("photoId:", photoId, "action:", action);

    console.log("USER:", user);

    if (user == "AnonymousUser") {
      addCookieItem(photoId, action);
    } else {
      updateUserOrder(photoId, action);
    }
  });
}

function addCookieItem(photoId, action) {
  console.log("Not logged in..");

  if (action == "add") {
    if (cart[photoId] == undefined) {
      cart[photoId] = { quantity: 1 };
    } else {
      cart[photoId]["quantity"] += 1;
    }
  }
  if (action == "remove") {
    cart[photoId]["quantity"] -= 1;

    if (cart[photoId]["quantity"] <= 0) {
      console.log("Remove Item");
      delete cart[photoId];
    }
  }
  console.log("Cart:", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(photoId, action) {
  console.log("User is logged in, sending data...");

  var url = "/updateItem/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "applicaion/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ photoId: photoId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Data:", data);
      location.reload();
    });
}
