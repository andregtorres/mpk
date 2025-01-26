<?php
  //Connect to database
  include("../include/dbConn.php");

  //Get current date and time
  $updated = date("Y-m-d");
  if(!empty($_POST['id'])){
    $id = test_input($_POST['id']);
    $times_from = test_input($_POST['times_from']);
    $times_to = test_input($_POST['times_to']);
    $stmt = $conn->prepare("UPDATE legs SET data_from = ?, data_to=?, updated=? WHERE id = ?");
    $stmt -> bind_param("ssss", $times_from, $times_to, $updated, $id);
    $stmt->execute();
    echo "DB OK\n";
    $stmt -> close();
  }  else {
    echo "Invalid request\n";
  }
  $conn->close();
?>
