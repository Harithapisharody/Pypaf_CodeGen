// script.js
document.getElementById("generateForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let userInput = document.getElementById("userInput").value.trim();

    const editableCodeElement = document.getElementById("editableCode");
    const generatedCodeHeading = document.getElementById("generatedCodeHeading");
    const copyButton = document.getElementById("copyButton");
    const runButton = document.getElementById("runButton");
    const generatedAlgorithmElement = document.getElementById("generatedAlgorithm");
    const generatedAlgorithmHeading = document.getElementById("generatedAlgorithmHeading");
    const generatedFlowchart = document.getElementById("generatedFlowchart");
    const flowchartImage = document.getElementById("flowchartImage");
    const generatedFlowchartHeading = document.getElementById("generatedFlowchartHeading");

    // Reset visibility and content
    editableCodeElement.style.display = 'none';
    editableCodeElement.value = '';
    copyButton.style.display = 'none';
    runButton.style.display = 'none';
    generatedAlgorithmElement.style.display = 'none';
    generatedAlgorithmElement.value = '';
    generatedFlowchart.style.display = 'none';
    flowchartImage.src = '';  // Reset flowchart image
    generatedFlowchartHeading.style.display = 'none';  // Hide flowchart heading initially
    generatedCodeHeading.style.display = 'none';
    generatedAlgorithmHeading.style.display = 'none';

    if (userInput) {
        try {
            const data = await postData('/generate', { logic: userInput });

            if (data.generated_code) {
                // Display generated code
                editableCodeElement.value = data.generated_code;
                generatedCodeHeading.style.display = 'block';
                editableCodeElement.style.display = 'block';
                copyButton.style.display = 'inline-block';
                runButton.style.display = 'inline-block';

                // Display generated algorithm
                if (data.algorithm) {
                    generatedAlgorithmElement.textContent = data.algorithm;
                    generatedAlgorithmHeading.style.display = 'block';
                    generatedAlgorithmElement.style.display = 'block';
                }

                // Display generated flowchart
                if (data.flowchart_filename) {
                    flowchartImage.src = `${baseURL}/${data.flowchart_filename}.png?t=${new Date().getTime()}`;
                    generatedFlowchart.style.display = 'block';
                    generatedFlowchartHeading.style.display = 'block';
                }
            } else if (data.error) {
                editableCodeElement.value = `Error: ${data.error}`;
                generatedCodeHeading.style.display = 'block';
                editableCodeElement.style.display = 'block';
            }
        } catch (error) {
            editableCodeElement.value = 'Error generating code.';
            editableCodeElement.style.display = 'block';
            generatedCodeHeading.style.display = 'block';
        }
    }
});

// Copy code to clipboard
document.getElementById("copyButton").addEventListener("click", function() {
    const code = document.getElementById("editableCode").value;
    navigator.clipboard.writeText(code).then(function() {
        alert('Code copied to clipboard!');
    }, function(err) {
        console.error('Error copying code: ', err);
    });
});

// Run edited code
document.getElementById("runButton").addEventListener("click", async function() {
    const code = document.getElementById("editableCode").value;

    try {
        const data = await postData('/run', { code: code });
        if (data.output) {
            alert('Output: ' + data.output);
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error running code.');
    }
});
