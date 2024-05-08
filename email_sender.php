<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $recaptcha_secret = getenv('RECAPTCHA_SECRET');
    $token = $_POST['recaptchaToken'];
    $response = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret={$recaptcha_secret}&response={$token}");
    $responseKeys = json_decode($response, true);

// Convert PHP array to JSON for JavaScript
    $jsonResponse = json_encode($responseKeys);
    $errorCodes = isset($responseKeys['error-codes']) ? json_encode($responseKeys['error-codes']) : '[]';

    echo "<script>
    console.log('TOP SECRET:', getenv('RECAPTCHA_SECRET'));
    console.log('reCAPTCHA Response:', JSON.parse('$jsonResponse'));
    console.log('Error Codes:', JSON.parse('$errorCodes'));
    </script>";

    if ($responseKeys["success"]) {
        if ($responseKeys["score"] >= 0.5) {
            $name = htmlspecialchars($_POST['name']);
            $email = htmlspecialchars($_POST['email']);
            $message = htmlspecialchars($_POST['question']);

            // Properly escape arguments to prevent command injection
            $name_escaped = escapeshellarg($name);
            $email_escaped = escapeshellarg($email);
            $message_escaped = escapeshellarg($message);

            // Construct and execute the command
            $command = "python3 /var/www/html/wiseowlspeech.com/email_sender.py $name_escaped $email_escaped $message_escaped";
            $output = shell_exec($command);

            if (strpos($output, "Success") !== false) {
                echo "no"; // "<script>alert('Your request has been submitted.');</script>";
            } else {
                echo "no"; // "<script>alert('Failed to send email. Please try again.');</script>";
            }
        } else {           
            // bot?
            echo "no"; // "<script>alert('Failed to send email. Please try again. Score: " . $responseKeys. " Success: " . ($responseKeys["success"] ? 'Yes' : 'No') . "');</script>";

        }
    } else {
        echo "no"; // "<script>alert('Failed to send email. Please try again. Score: " . $responseKeys. " Success: " . ($responseKeys["success"] ? 'Yes' : 'No') . "');</script>";
    }
}
?>