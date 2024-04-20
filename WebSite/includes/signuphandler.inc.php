<?php

$host = "svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com";
$dbname = "database_e8ebb";
$dbusername = "shiftwallet";
$password = "1SuhdjXZxoByHWLWsWQk7bXyXSgMO4xS";
$port = "3333";

$conn = mysqli_init();

if (!$conn) {
    die('mysqli_init failed');
}

mysqli_ssl_set($conn, 'NULL', NULL, '../singlestore_bundle.pem', NULL, NULL);

// Tentar estabelecer uma conexão segura
if (!mysqli_real_connect($conn, $host, $dbusername, $password, $dbname, $port, NULL, MYSQLI_CLIENT_SSL)) {
    die('Connection Error: ' . mysqli_connect_error());
}

if($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $email = $_POST["email"];
    $phonenumber = $_POST["phonenumber"];
    $pwd = $_POST["password"];

    try {

        $sql_email = "SELECT * FROM Users WHERE email = '$email'";
        $result_email = $conn->query($sql_email);

        $sql_phonenumber = "SELECT * FROM Users WHERE phonenumber = '$phonenumber'";
        $result_phonenumber = $conn->query($sql_phonenumber);

        $sql_username = "SELECT * FROM Users WHERE name = '$username'";
        $result_username = $conn->query($sql_username);

        if ($result_email->num_rows > 0) {
            $error_message = "This email is already used by another user!";
            header("Location: ../register/register.html?error=" . urlencode($error_message));
            exit();
        }else if ($result_phonenumber->num_rows > 0) {
            $error_message = "This phone number is already used by another user!";
            header("Location: ../register/register.html?error=" . urlencode($error_message));
            exit();
        }else if ($result_username->num_rows > 0) {
            $error_message = "This username is already used by another person!";
            header("Location: ../register/register.html?error=" . urlencode($error_message));
            exit();
        }else {
            $query = "INSERT INTO Users (name, email, password, phonenumber) VALUES (?, ?, ?, ?)";
            
            $stmt = mysqli_stmt_init($conn);

            if(!mysqli_stmt_prepare($stmt, $query)) {
                die(mysqli_error($conn));
            }

            $hashed_password = password_hash($pwd, PASSWORD_DEFAULT);

            mysqli_stmt_bind_param($stmt, "sssi", $username, $email, $hashed_password, $phonenumber);
            
            mysqli_stmt_execute($stmt);

            header("Location: ../index.html");
        }

    } catch (PDOException $e) {
        die("Query Failed: " . $e->getMessage());
    }
}else {
    header("Location: ../index.html");
}