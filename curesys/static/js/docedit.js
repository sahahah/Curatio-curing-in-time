document.addEventListener("DOMContentLoaded", function() {
    // Retrieve user details from local storage
    var firstName1 = localStorage.getItem('firstName');
    var lastName1 = localStorage.getItem('lastName');
    var email1 = localStorage.getItem('email');
    var phone1 = localStorage.getItem('phone');
    var mobile1 = localStorage.getItem('mobile');
    var address1 = localStorage.getItem('address');
    var dob1 = localStorage.getItem('dob');

    // Display user details in the HTML
    document.getElementById('firstNameValue').innerHTML = firstName1;
    document.getElementById('lastNameValue').innerHTML = lastName1;
    document.getElementById('emailValue').innerHTML = email1;
    document.getElementById('phoneValue').innerHTML = phone1;
    document.getElementById('mobileValue').innerHTML = mobile1;
    document.getElementById('addressValue').innerHTML = address1;
    document.getElementById('dobValue').innerHTML = dob1;
});

// Function to save a note
function saveNote() {
    const noteText = document.getElementById('noteText').value.trim();
    if (noteText === "") {
      alert("Please enter a note before saving.");
      return;
    }

    // Get existing notes from localStorage
    const savedNotes = JSON.parse(localStorage.getItem('savedNotes')) || [];

    // Add the new note to the list
    savedNotes.push(noteText);

    // Save the updated list back to localStorage
    localStorage.setItem('savedNotes', JSON.stringify(savedNotes));

    // Clear the textarea
    document.getElementById('noteText').value = "";

    // Refresh the list of saved notes
    displaySavedNotes();
  }

  // Function to display saved notes
  function displaySavedNotes() {
    const savedNotesContainer = document.getElementById('savedNotes');
    savedNotesContainer.innerHTML = "";

    // Get saved notes from localStorage
    const savedNotes = JSON.parse(localStorage.getItem('savedNotes')) || [];

    // Display each saved note in a list item
    savedNotes.forEach((note, index) => {
      const listItem = document.createElement('li');
      listItem.className = 'list-group-item';
      listItem.textContent = note;

      // Add delete button for each note
      const deleteButton = document.createElement('button');
      deleteButton.className = 'btn btn-danger btn-sm float-right';
      deleteButton.textContent = 'Delete';
      deleteButton.onclick = () => deleteNote(index);

      listItem.appendChild(deleteButton);
      savedNotesContainer.appendChild(listItem);
    });
  }

  // Function to delete a note
  function deleteNote(index) {
    // Get saved notes from localStorage
    const savedNotes = JSON.parse(localStorage.getItem('savedNotes')) || [];

    // Remove the note at the specified index
    savedNotes.splice(index, 1);

    // Save the updated list back to localStorage
    localStorage.setItem('savedNotes', JSON.stringify(savedNotes));

    // Refresh the list of saved notes
    displaySavedNotes();
  }

  // Display saved notes on page load
  displaySavedNotes();