
function goToPage2() {
    window.location.href = 'allergies.html';
}

function goToPage3() {
    window.location.href = 'immune.html';
}
function goToPage4() {
    window.location.href = 'vitals.html';
}
function goToPage5() {
    window.location.href = 'heart.html';
}
function goToPage6() {
    window.location.href = 'resp.html';
}
function goToPage7() {
    window.location.href = 'diag.html';
}
function goToPage8() {
    window.location.href = 'surgery.html';
}

function openMedicationForm() {
    document.getElementById("medicationForm").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closeMedicationForm() {
    document.getElementById("medicationForm").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function submitAllergyForm() {
    // Get form values
    var patientName = document.getElementById("patientName").value;
    var patientID = document.getElementById("patientID").value;
    var allergyType = document.getElementById("allergyType").value;
    var allergen = document.getElementById("allergen").value;
    var reaction = document.getElementById("reaction").value;
    var additionalInfo = document.getElementById("additionalInfo").value;
    var doctorName = document.getElementById("doctorName").value;
    var dosage = document.getElementById("dosage").value;

    // Create an object with form values
    var allergyData = {
        patientName: patientName,
        patientID: patientID,
        allergyType: allergyType,
        allergen: allergen,
        reaction: reaction,
        additionalInfo: additionalInfo,
        doctorName: doctorName,
        dosage: dosage
    };

    var savedData = JSON.parse(localStorage.getItem('allergyData')) || [];

    savedData.push(allergyData);

    localStorage.setItem('allergyData', JSON.stringify(savedData));

    var cardContent = `
        <h2>${allergyType} Allergy</h2>
        <p><strong>Patient Name:</strong> ${patientName}</p>
        <p><strong>Patient ID:</strong> ${patientID}</p>
        <p><strong>Allergen:</strong> ${allergen}</p>
        <p><strong>Reaction:</strong> ${reaction}</p>
        <p><strong>Additional Information:</strong> ${additionalInfo}</p>
        <p><strong>Doctor Name:</strong> ${doctorName}</p>
        <p><strong>Dosage:</strong> ${dosage}</p>
    `;

    var cardDiv = document.createElement("div");
    cardDiv.classList.add("card");
    cardDiv.innerHTML = cardContent;

    var card1Section = document.querySelector(".card1");
    card1Section.appendChild(cardDiv);

    closeMedicationForm();
}
