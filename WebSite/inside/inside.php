<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shift Wallet | Your Account</title>
    
    <link rel="stylesheet" href="styles/style-inside.css">
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="styles/media-query-inside.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    
    <link rel="shortcut icon" href="../images/favicon.ico" type="image/x-icon">
    
</head>
<body class="conteiner">

    <?php

    if (!isset($_COOKIE['username'])) {
        header("Location: ../login/login.html");
        exit(); 
    }

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

    $username = $_COOKIE['username'];
    $query = "SELECT id FROM Users WHERE name = '$username'";
    $result = mysqli_query($conn, $query);

    if ($result) {
        $row = mysqli_fetch_assoc($result);
        
        $id = $row['id'];
        
        $query = "SELECT balance FROM Cards WHERE user_id = '$id'";
        $result = mysqli_query($conn, $query);
        
        if ($result) {
            $row = mysqli_fetch_assoc($result);
            
            $balance = $row['balance'];
        }
    } else {
        echo 'Erro ao buscar saldo: ' . mysqli_error($conn);
    }

    mysqli_close($conn);
    ?>

    <header>
        <div class="header">
            <img src="../images/favicon.ico" class="logo">

            <h1>Shift Wallet</h1>

            <p id="username"></p>
            </div>
    </header>

    <main class="content">
        <div class="content">
            <p id="balance">0 €</p>

            <a href="#">Transfer</a>
            <a href="#">Deposit</a>
            <a href="#">Withdraw</a>
            <a href="#">Safe</a>
            
            <a href="#" id="logout" onclick="limparCookies()">Log out</a>
        </div>
    </main>

    <footer>
        <h2>Shift Wallet &#169</h2>

        <div class="socials">
            <a href="#" class="fa fa-facebook"></a>
            <a href="#" class="fa fa-twitter"></a>
            <a href="#" class="fa fa-instagram"></a>
            <a href="#" class="fa fa-linkedin"></a>
        </div>
    </footer>

    <script>
    document.getElementById('balance').innerText = '<?php echo $balance; ?> €';
    document.getElementById('username').innerText = '<?php echo $username; ?>';
    </script>
    
    <script src="script-inside.js"></script>
</body>
</html>