<?php
  //Connect to database
  include("../include/dbConn.php");

  //Get current date and time
  $stmt = $conn->prepare("SELECT id, line, stop_from_direction, stop_from_idx, stop_to_direction, stop_to_idx, stop_to_offset, updated  FROM legs");
  $stmt->execute();
  $result = $stmt->get_result();
  $stmt -> close();
  $out_array=array();
  while($row = $result->fetch_assoc()) {
    $out_array[]=$row;
  }
  #$out_array = array("host"=>$id, "day"=>$day_input->format("Y-m-d"),"time"=>$time_array,"temp"=>$temp_array,"humi"=>$humi_array);
  echo json_encode($out_array);
  $conn->close();
?>
