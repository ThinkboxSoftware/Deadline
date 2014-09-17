<?php
        $server = "http://192.168.2.186:8080";

        // create curl resource
        print("Initializing\n");
        $ch = curl_init($server . "/api/jobs");

        // create Deadline JSON request structure
        $data = array(
            'Command' => 'requeue',
            'JobID' => '53ed30b6f4b70d991c6a3be0'
            );
            
        $json_data = json_encode($data);
            
        print("Sending " . $json_data . "\n");

        // set up curl to do what we want
        curl_setopt_array($ch, array(
            CURLOPT_CUSTOMREQUEST => "PUT",
            CURLOPT_RETURNTRANSFER => TRUE,
            CURLOPT_HTTPHEADER => array(
                'Content-Type: application/json'
            ),
            CURLOPT_POSTFIELDS => json_encode($data)
        ));

        print("Executing request\n");
        $output = curl_exec($ch);
        
        print("\n");
        print $output;
        print("\n");

        // close curl resource to free up system resources
        print("Closing\n");
        curl_close($ch);
?>
