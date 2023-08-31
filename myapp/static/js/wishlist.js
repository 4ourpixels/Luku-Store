var updateBtns = document.getElementsByClassName("update-wishlist");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "action:", action);

    console.log("USER:", user);

    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserWishlist(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("Not logged in..");

  if (action == "add") {
    if (wishlist[productId] == undefined) {
      wishlist[productId] = { quantity: 1 };
    } else {
      wishlist[productId]["quantity"] += 1;
    }
  }
  if (action == "remove") {
    wishlist[productId]["quantity"] -= 1;

    if (wishlist[productId]["quantity"] <= 0) {
      console.log("Remove Item");
      delete wishlist[productId];
    }
  }
  console.log("Wishlist:", wishlist);
  document.cookie = "wishlist=" + JSON.stringify(wishlist) + ";domain=;path=/";
  location.reload();
}

function updateUserWishlist(productId, action) {
  console.log("User is logged in, sending data...");

  var url = "/updateWishlist/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "applicaion/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Data:", data);
      location.reload();
    });
}
