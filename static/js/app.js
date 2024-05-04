function estimatePrice() {
  var sqft = $("#uiSqft").val();
  var bhk = $("input[name='uiBHK']:checked").val();
  var bath = $("input[name='uiBathrooms']:checked").val();
  var location = $("#uiLocations").val();

  $.ajax({
    type: "POST",
    url: "/predict_home_price",
    data: {
      Squareft: sqft,
      uiBHK: bhk,
      uiBathrooms: bath,
      uiLocations: location,
    },
    success: function (response) {
      $("#uiEstimatedPrice h2").text(
        "Estimated Price: " + response.estimated_price
      );
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

$(document).ready(function () {
  // Fetch location names and populate dropdown
  $.get("/get_location_names", function (data) {
    data.locations.forEach(function (location) {
      $("#uiLocations").append("<option>" + location + "</option>");
    });
  });
});
