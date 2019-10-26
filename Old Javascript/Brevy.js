// ********* NEEDS TO GO IN MAIN
function trimWhitespace(x) {
  return x.replace(/^\s+|\s+$/gm, '');
}
// ****** ABOVE NEEDS TO GO IN MAIN

var APAAuthTarget = document.getElementById("Brevy-AuthorsAPA"),
  ChicagoAuthTarget = document.getElementById("Brevy-AuthorsChicago"),
  MLAAuthTarget = document.getElementById("Brevy-AuthorsMLA");

function authArraySetup(authtarget) {

  // Gets rid of all periods and splits into an array by commas
  var authparse = authtarget.innerHTML.replace(/\./g, "").split(",");
  // The output holder which will be used to set the final html
  var authoutput = "";

  // Trims whitespace out of either side of the function
  for (i = 0; i < authparse.length; i++) {
    authparse[i] = trimWhitespace(authparse[i]);
  }

  // Splits the array into an array of arrays via splitting by spaces
  for (i = 0; i < authparse.length; i++) {
    authparse[i] = authparse[i].split(" ");
  }

  // For APA style
  if (authtarget == APAAuthTarget) {
    for (i = 0; i < authparse.length; i++) {
      // First must be different due to possible commas
      if (i == 0) {
        if (authparse[i].length == 1) { // Presume is last name only
          authoutput += authparse[i][0];
        } else if (authparse[i].length == 2) { // Presume is first & last
          authoutput += authparse[i][1] +
            ", " + authparse[i][0].slice(0, 1) + ".";
        } else if (authparse[i].length == 3) { // Presume is first, middle, last
          authoutput += authparse[i][2] +
            ", " + authparse[i][0].slice(0, 1) + ". " + authparse[i][1].slice(0, 1) + ".";
        }
      }
      // This is the general handling for the APA style though
      else if (i != 0 && i != authparse.length - 1 && authparse[i][0] + " " + authparse[i][1] != "et al") {
        if (authparse[i].length == 1) { // Presume is last name only
          authoutput += authparse[i][0];
        } else if (authparse[i].length == 2) { // Presume is first & last
          authoutput += ", " + authparse[i][1] +
            ", " + authparse[i][0].slice(0, 1) + ".";
        } else if (authparse[i].length == 3) { // Presume is first, middle, last
          authoutput += ", " + authparse[i][2] +
            ", " + authparse[i][0].slice(0, 1) + ". " + authparse[i][1].slice(0, 1) + ".";
        }
      }
      // The last needs to be differnt due to the & sign
      else if (i == authparse.length - 1 && authparse[i][0] + " " + authparse[i][1] != "et al") {
        if (authparse[i].length == 1) { // Presume is last name only
          authoutput += ", & " + authparse[i][0];
        } else if (authparse[i].length == 2) { // Presume is first & last
          authoutput += ", & " + authparse[i][1] +
            ", " + authparse[i][0].slice(0, 1) + ".";
        } else if (authparse[i].length == 3) { // Presume is first, middle, last
          authoutput += ", & " + authparse[i][2] +
            ", " + authparse[i][0].slice(0, 1) + ". " + authparse[i][1].slice(0, 1) + ".";
        }
      }
      // Takes into account et all which may come from the autofill
      else {
        authoutput += ", & et al";
      }
    }
    // Append a period to cap the end if it doesn't have one
    if (authoutput.slice(-1) != ".") {
      authoutput += "."
    }
    // Finally set the overall results
    APAAuthTarget.innerHTML = authoutput;
  }

  // For Chicago style
  if (authtarget == ChicagoAuthTarget) {
    for (i = 0; i < authparse.length; i++) {
      // First must be different as last name, first name mid.,
      if (i == 0) {
        if (authparse[0].length == 1) { // Presume is last name only
          authoutput += authparse[0][0];
        } else if (authparse[0].length == 2) { // Presume is first & last
          authoutput += authparse[0][1] +
            ", " + authparse[0][0];
        } else if (authparse[0].length == 3) { // Presume is first, middle, last
          authoutput += authparse[0][2] +
            ", " + authparse[0][0] + " " + authparse[0][1].slice(0, 1) + ".";
        }
      }
      // The general handling for the middle authors is First Mid. Last,
      else if (i != 0 && i != authparse.length - 1 && authparse[i][0] + " " + authparse[i][1] != "et al") {
        if (authparse[i].length == 1) { // Presume is last name only
          authoutput += ", " + authparse[i][0];
        } else if (authparse[i].length == 2) { // Presume is first & last
          authoutput += ", " + authparse[i][0] +
            " " + authparse[i][1];
        } else if (authparse[i].length == 3) { // Presume is first, middle, last
          authoutput += ", " + authparse[i][0] +
            " " + authparse[i][1].slice(0, 1) + ". " + authparse[i][2];
        }
      }
      // Last author is different as there is an "and" before it
      else if (i == authparse.length - 1 && authparse[i][0] + " " + authparse[i][1] != "et al") {
        if (authparse[i].length == 1) { // Presume is last name only
          authoutput += ", and " + authparse[i][0];
        } else if (authparse[i].length == 2) { // Presume is first & last
          authoutput += ", and " + authparse[i][0] +
            " " + authparse[i][1];
        } else if (authparse[i].length == 3) { // Presume is first, middle, last
          authoutput += ", and " + authparse[i][0] +
            " " + authparse[i][1].slice(0, 1) + ". " + authparse[i][2];
        }
      }
      // Takes into account et all which may come from the autofill
      else {
        authoutput += ", and et al";
      }
    }
    // Append a period to cap the end if it doesn't have one
    if (authoutput.slice(-1) != ".") {
      authoutput += "."
    }
    // Finally set the overall results
    ChicagoAuthTarget.innerHTML = authoutput;
  }

  // For MLA style
  if (authtarget == MLAAuthTarget) {
    // First must be different as last name, first name mid.,
    if (authparse.length > 0) {
      if (authparse[0].length == 1) { // Presume is last name only
        authoutput += authparse[0][0];
      } else if (authparse[0].length == 2) { // Presume is first & last
        authoutput += authparse[0][1] +
          ", " + authparse[0][0];
      } else if (authparse[0].length == 3) { // Presume is first, middle, last
        authoutput += authparse[0][2] +
          ", " + authparse[0][0] + " " + authparse[0][1].slice(0, 1) + ".";
      }
    }
    // Other authors than first are first name mid. last name, with an "and" before the final author
    // This is for the 2nd of two authors
    if (authparse.length == 2) {
      if (authparse[1].length == 1) { // Presume is last name only
        authoutput += ", and " + authparse[1][0];
      } else if (authparse[1].length == 2) { // Presume is first & last
        authoutput += ", and " + authparse[1][0] +
          " " + authparse[1][1];
      } else if (authparse[1].length == 3) { // Presume is first, middle, last
        authoutput += ", and " + authparse[1][0] +
          " " + authparse[1][1].slice(0, 1) + ". " + authparse[1][2];
      }
    }
    // Other authors than first are first name mid. last name, with an "and" before the final author
    if (authparse.length == 3) {
      // This is for the 2nd of three authors
      if (authparse[1].length == 1) { // Presume is last name only
        authoutput += ", " + authparse[1][0];
      } else if (authparse[1].length == 2) { // Presume is first & last
        authoutput += ", " + authparse[1][0] +
          " " + authparse[1][1];
      } else if (authparse[1].length == 3) { // Presume is first, middle, last
        authoutput += ", " + authparse[1][0] +
          " " + authparse[1][1].slice(0, 1) + ". " + authparse[1][2];
      }
      // This is for the 3rd of three authors
      if (authparse[2].length == 1) { // Presume is last name only
        authoutput += ", and " + authparse[2][0];
      } else if (authparse[2].length == 2) { // Presume is first & last
        authoutput += ", and " + authparse[2][0] +
          " " + authparse[2][1];
      } else if (authparse[2].length == 3) { // Presume is first, middle, last
        authoutput += ", and " + authparse[2][0] +
          " " + authparse[2][1].slice(0, 1) + ". " + authparse[2][2];
      }
    }
    // If more than three authors, just do first and then et al
    if (authparse.length > 3) {
      authoutput += ", and et al";
    }
    // Append a period to cap the end if it doesn't have one
    if (authoutput.slice(-1) != ".") {
      authoutput += "."
    }
    // Finally set the overall results
    MLAAuthTarget.innerHTML = authoutput;
  }

}

// Calls the above function to change the author displays
authArraySetup(APAAuthTarget);
authArraySetup(ChicagoAuthTarget);
authArraySetup(MLAAuthTarget);
