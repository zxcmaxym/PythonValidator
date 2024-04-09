document.getElementById("uploadForm").addEventListener("submit", function(event) {
  event.preventDefault();
  
  var formData = new FormData();
  var fileInput = document.getElementById("fileInput").files[0];
  formData.append("file", fileInput);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:4444/hehe", true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      document.getElementById("statusMsg").innerText = "File uploaded successfully!";
    } else {
      document.getElementById("statusMsg").innerText = "Error uploading file.";
    }
  };
  xhr.send(formData);
});

