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

mysqli_ssl_set($conn, NULL, NULL, '../singlestore_bundle.pem', NULL, NULL);

if (!mysqli_real_connect($conn, $host, $dbusername, $password, $dbname, $port, NULL, MYSQLI_CLIENT_SSL)) {
    die('Connection Error: ' . mysqli_connect_error());
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $pwd = $_POST["password"];

    try {
        $sql = "SELECT * FROM Users WHERE email = ?";
        
        $stmt = mysqli_stmt_init($conn);
        if (!mysqli_stmt_prepare($stmt, $sql)) {
            die(mysqli_error($conn));
        }

        mysqli_stmt_bind_param($stmt, "s", $email);
        mysqli_stmt_execute($stmt);

        $result = mysqli_stmt_get_result($stmt);

        if ($row = mysqli_fetch_assoc($result)) {
            if (password_verify($pwd, $row['password'])) {
                header("Location: ../index.html");
                exit();
            } else {
                $error_message = "Username or password incorrect, try again!";
                header("Location: ../login/login.html?error=" . urlencode($error_message));
                exit();
            }
        } else {
            $error_message = "Username or password incorrect, try again!";
            header("Location: ../login/login.html?error=" . urlencode($error_message));
            exit();
        }
    } catch (PDOException $e) {
        die("Query Failed: " . $e->getMessage());
    }
} else {
    header("Location: ../index.html");
}
?>
