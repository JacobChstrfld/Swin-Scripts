function dadabik_updateTitles(field) {
    // Get the selected department name
    field = document.querySelector('[name="emp_dname"]');
    var selectedOption = field.options[field.selectedIndex];
    var selectedDepartment = selectedOption.text;
    //console.log("selectedDepartment" + selectedDepartment)

    title = document.querySelector('[name="emp_title"]');
    if (title !== null){
        var titleOption = title.options[title.selectedIndex];
    }

    // Perform the first AJAX request to get the department code
    $.ajax({
        url: 'getDcode.php', // PHP file to get the department code
        method: 'POST',
        data: { department_name: selectedDepartment },
        success: function(dcodeResponse) {
            // Update the department_code field with the retrieved value
            var dcode = document.querySelector('[name="emp_dcode"]');
            dcode.value = dcodeResponse;

            // Perform the second AJAX request to get job titles using the department code
            $.ajax({
                url: 'getTitles.php', // PHP file to get job titles
                method: 'POST',
                data: { department_code: dcodeResponse },
                success: function(titlesResponse) {
                    // Parse the JSON response
                    var jobTitles = JSON.parse(titlesResponse);

                    // Get the job titles list element (replace 'upjob_titles_list' with your actual ID or selector)
                    var jobTitlesList = document.querySelector('[name="emp_title"]');
                    jobTitlesList.innerHTML = ''; // Clear existing list items
                    var placeholderOption = document.createElement('option');
                    placeholderOption.text = '';
                    placeholderOption.value = '';
                    placeholderOption.selected = true; // Ensure this option is selected by default
                    // placeholderOption.disabled = true; // Make it non-selectable
                    jobTitlesList.appendChild(placeholderOption);
                    for (var i = 0; i < jobTitles.length; i++) {
                        var option = document.createElement('option');
                        option.value = jobTitles[i].job_id;
                        option.text = jobTitles[i].title;
                        console.log(jobTitles[i].title + " " + titleOption.text)
                        if(jobTitles[i].title.toLowerCase() === titleOption.text.toLowerCase()){
                            option.selected = true;
                        }
                        jobTitlesList.appendChild(option);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("AJAX Error: " + status + ": " + error);
                }
            });
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: " + status + ": " + error);
        }
    });
}
document.addEventListener('DOMContentLoaded', function() {
    field = document.querySelector('[name="emp_title"]');
    if(field === null){
       // console.log("Field doesn't exist on this page");
    }
    else{
        document.querySelector('[name="emp_dcode"]').readOnly = true;
        var selectedOption1 = field.options[field.selectedIndex];
        var selectedTitle = selectedOption1.text;
        dname = document.querySelector('[name="emp_dname"]');
        var selectedOption2 = dname.options[dname.selectedIndex];
        var selectedDname = selectedOption2.text;

        if(selectedTitle !== null && selectedDname !== ""){
             dadabik_updateTitles("h");
        }
    }
});
