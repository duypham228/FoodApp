document.getElementById("addItemButton").addEventListener("click", function () {
  const itemId = document.getElementById("itemId").value;
  const quantity = document.getElementById("quantity").value;

  if (itemId && quantity) {
    const appendedData = document.getElementById("appendedData");
    const itemDiv = document.createElement("div");
    itemDiv.innerHTML = `
      <input type="hidden" name="itemIds" value="${itemId}">
      <input type="hidden" name="quantities" value="${quantity}">
    `;
    const itemDivInfo = document.createElement("div");
    itemDivInfo.innerHTML = `
      <p>Item ID: ${itemId} - Quantity: ${quantity}</p>
      <br>
    `;
    appendedData.appendChild(itemDiv);
    appendedData.appendChild(itemDivInfo);

    // Clear the input fields
    document.getElementById("itemId").value = "";
    document.getElementById("quantity").value = "";
  }
});
