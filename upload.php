<?php
// Check if the file was uploaded without errors
if ($_FILES["file"]["error"] == UPLOAD_ERR_OK) {
    // Specify the destination directory
    $uploadDir = './testenv/StudentWork/';

    // Get the temporary file path
    $tmpFilePath = $_FILES["file"]["tmp_name"];

    // Get the original file name
    $fileName = $_FILES["file"]["name"];

    // Build the destination path
    $destFilePath = $uploadDir . $fileName;

    // Move the uploaded file to the destination directory
    if (move_uploaded_file($tmpFilePath, $destFilePath)) {
        // File uploaded successfully
        echo "File uploaded successfully!";
    } else {
        // Error moving file
        echo "Error moving file.";
    }
} else {
    // Error uploading file
    echo "Error uploading file.";
}
?>

