
    function submitBloodPressure() {
        var systolic = document.getElementById("systolic").value;
        var diastolic = document.getElementById("diastolic").value;
        var bloodPressureValue = systolic + "/" + diastolic + " mmHg";
        document.getElementById("bloodPressureValue").textContent = bloodPressureValue;
        document.getElementById("bloodPressureResult").style.display = "block";
        $('#bloodPressureModal').modal('hide');
    }

    function submitHeartRate() {
       
        var heartrate = document.getElementById("heartrate").value;
        var heartrateValue =  heartrate + "bpm";
        
        document.getElementById("heartrateResult").style.display = "block";
        $('#heartrateModal').modal('hide');
    }

    function showMore(type) {
        // You can implement the view more functionality here
        alert("View More functionality for " + type + " vitals");
    }