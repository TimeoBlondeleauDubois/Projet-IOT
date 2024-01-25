<?php

// Connexion à la base de données SQLite
try {
    $db = new PDO('sqlite:base_de_donnee.db');
} catch (PDOException $e) {
    die('Connexion échouée : ' . $e->getMessage());
}

// Récupération des données depuis la requête GET
$temperature = isset($_GET['temperature']) ? floatval($_GET['temperature']) : null;
$humidity = isset($_GET['humidity']) ? floatval($_GET['humidity']) : null;
$pressure = isset($_GET['pressure']) ? floatval($_GET['pressure']) : null;

// Vérification des données
if ($temperature !== null && $humidity !== null && $pressure !== null) {
    // Insertion des données dans la table Meteo
    $stmt = $db->prepare("INSERT INTO Meteo (temperature, humidity, pressure, temps) VALUES (:temperature, :humidity, :pressure, datetime('now'))");
    $stmt->bindParam(':temperature', $temperature);
    $stmt->bindParam(':humidity', $humidity);
    $stmt->bindParam(':pressure', $pressure);

    if ($stmt->execute()) {
        echo "Données enregistrées avec succès dans la base de données.";
    } else {
        echo "Erreur lors de l'enregistrement des données.";
    }
} else {
    echo "Données manquantes.";
}

// Fermeture de la connexion à la base de données
$db = null;

?>
