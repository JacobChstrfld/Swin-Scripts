<?php
// Database connection settings
$host = 'localhost';
$db = 'swinomish_acl';
$user = 'redacted';
$pass = 'redacted';

try {
    // Create a new PDO instance
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Get the department code from the AJAX request
    $department_code = $_POST['department_code'];

    // Prepare and execute the query to fetch job titles and job_ids
    $stmt = $pdo->prepare('SELECT job_id, title FROM job_titles WHERE job_dcode = ?');
    $stmt->execute([$department_code]);
    $job_titles = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Output the job titles as JSON
    echo json_encode($job_titles);
} catch (PDOException $e) {
    // Log any errors
    error_log('Connection failed: ' . $e->getMessage());
}
?>
