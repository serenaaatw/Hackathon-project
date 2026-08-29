USE defaultdb;
-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: hackathon
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id_category` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id_category`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'animales','Animales'),(2,'acciones','Acciones');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learning_round_words`
--

DROP TABLE IF EXISTS `learning_round_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learning_round_words` (
  `id_round_word` int(11) NOT NULL AUTO_INCREMENT,
  `id_round` int(11) NOT NULL,
  `id_word` int(11) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id_round_word`),
  KEY `id_round` (`id_round`),
  KEY `id_word` (`id_word`),
  CONSTRAINT `learning_round_words_ibfk_1` FOREIGN KEY (`id_round`) REFERENCES `learning_rounds` (`id_round`),
  CONSTRAINT `learning_round_words_ibfk_2` FOREIGN KEY (`id_word`) REFERENCES `words` (`id_word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learning_round_words`
--

LOCK TABLES `learning_round_words` WRITE;
/*!40000 ALTER TABLE `learning_round_words` DISABLE KEYS */;
/*!40000 ALTER TABLE `learning_round_words` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learning_rounds`
--

DROP TABLE IF EXISTS `learning_rounds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learning_rounds` (
  `id_round` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_category` int(11) NOT NULL,
  `fase` varchar(30) NOT NULL,
  `juego_actual` int(11) NOT NULL,
  `completada` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_round`),
  KEY `id_user` (`id_user`),
  KEY `id_category` (`id_category`),
  CONSTRAINT `learning_rounds_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `learning_rounds_ibfk_2` FOREIGN KEY (`id_category`) REFERENCES `categories` (`id_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learning_rounds`
--

LOCK TABLES `learning_rounds` WRITE;
/*!40000 ALTER TABLE `learning_rounds` DISABLE KEYS */;
/*!40000 ALTER TABLE `learning_rounds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `progress` (
  `id_progress` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_word` int(11) NOT NULL,
  `aciertos` int(11) NOT NULL,
  `intentos` int(11) NOT NULL,
  `dominio` int(11) NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `ronda` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_progress`),
  KEY `id_user` (`id_user`),
  KEY `id_word` (`id_word`),
  CONSTRAINT `progress_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `progress_ibfk_2` FOREIGN KEY (`id_word`) REFERENCES `words` (`id_word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

LOCK TABLES `progress` WRITE;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sentence_progress`
--

DROP TABLE IF EXISTS `sentence_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentence_progress` (
  `id_sentence_progress` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_sentence` int(11) NOT NULL,
  `aciertos` int(11) NOT NULL,
  `intentos` int(11) NOT NULL,
  `dominio` int(11) NOT NULL,
  `ronda` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_sentence_progress`),
  KEY `id_user` (`id_user`),
  KEY `id_sentence` (`id_sentence`),
  CONSTRAINT `sentence_progress_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `sentence_progress_ibfk_2` FOREIGN KEY (`id_sentence`) REFERENCES `sentences` (`id_sentence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentence_progress`
--

LOCK TABLES `sentence_progress` WRITE;
/*!40000 ALTER TABLE `sentence_progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `sentence_progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sentence_words`
--

DROP TABLE IF EXISTS `sentence_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentence_words` (
  `id_sentence_word` int(11) NOT NULL AUTO_INCREMENT,
  `id_sentence` int(11) NOT NULL,
  `id_word` int(11) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id_sentence_word`),
  KEY `id_sentence` (`id_sentence`),
  KEY `id_word` (`id_word`),
  CONSTRAINT `sentence_words_ibfk_1` FOREIGN KEY (`id_sentence`) REFERENCES `sentences` (`id_sentence`),
  CONSTRAINT `sentence_words_ibfk_2` FOREIGN KEY (`id_word`) REFERENCES `words` (`id_word`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentence_words`
--

LOCK TABLES `sentence_words` WRITE;
/*!40000 ALTER TABLE `sentence_words` DISABLE KEYS */;
INSERT INTO `sentence_words` VALUES (1,1,1,1),(2,1,6,2),(3,2,1,1),(4,2,7,2),(5,3,1,1),(6,3,8,2),(7,4,2,1),(8,4,6,2),(9,5,2,1),(10,5,7,2),(11,6,2,1),(12,6,8,2),(13,7,4,1),(14,7,6,2),(15,8,4,1),(16,8,7,2),(17,9,4,1),(18,9,8,2),(19,10,3,1),(20,10,6,2),(21,11,3,1),(22,11,7,2),(23,12,3,1),(24,12,8,2),(25,13,5,1),(26,13,6,2),(27,14,5,1),(28,14,7,2),(29,15,5,1),(30,15,8,2);
/*!40000 ALTER TABLE `sentence_words` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sentences`
--

DROP TABLE IF EXISTS `sentences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentences` (
  `id_sentence` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(255) NOT NULL,
  `id_subject` int(11) NOT NULL,
  `id_action` int(11) NOT NULL,
  `image_file` varchar(255) DEFAULT NULL,
  `lsa_video_file` varchar(255) DEFAULT NULL,
  `sentence_video_file` varchar(255) DEFAULT NULL,
  `audio_file` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_sentence`),
  KEY `id_subject` (`id_subject`),
  KEY `id_action` (`id_action`),
  CONSTRAINT `sentences_ibfk_1` FOREIGN KEY (`id_subject`) REFERENCES `words` (`id_word`),
  CONSTRAINT `sentences_ibfk_2` FOREIGN KEY (`id_action`) REFERENCES `words` (`id_word`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentences`
--

LOCK TABLES `sentences` WRITE;
/*!40000 ALTER TABLE `sentences` DISABLE KEYS */;
INSERT INTO `sentences` VALUES (1,'EL PERRO COME',1,6,'perro_come.png','lsa_perro_come.mp4','perro_come.mp4','el_perro_come.mp3'),(2,'EL PERRO DUERME',1,7,'perro_duerme.png','lsa_perro_duerme.mp4','perro_duerme.mp4','el_perro_duerme.mp3'),(3,'EL PERRO JUEGA',1,8,'perro_juega.png','lsa_perro_juega.mp4','perro_juega.mp4','el_perro_juega.mp3'),(4,'EL GATO COME',2,6,'gato_come.png','lsa_gato_come.mp4','gato_come.mp4','el_gato_come.mp3'),(5,'EL GATO DUERME',2,7,'gato_duerme.png','lsa_gato_duerme.mp4','gato_duerme.mp4','el_gato_duerme.mp3'),(6,'EL GATO JUEGA',2,8,'gato_juega.png','lsa_gato_juega.mp4','gato_juega.mp4','el_gato_juega.mp3'),(7,'EL P├üJARO COME',4,6,'pajaro_come.png','lsa_pajaro_come.mp4','pajaro_come.mp4','el_pajaro_come.mp3'),(8,'EL P├üJARO DUERME',4,7,'pajaro_duerme.png','lsa_pajaro_duerme.mp4','pajaro_duerme.mp4','el_pajaro_duerme.mp3'),(9,'EL P├üJARO JUEGA',4,8,'pajaro_juega.png','lsa_pajaro_juega.mp4','pajaro_juega.mp4','el_pajaro_juega.mp3'),(10,'EL PEZ COME',3,6,'pez_come.png','lsa_pez_come.mp4','pez_come.mp4','el_pez_come.mp3'),(11,'EL PEZ DUERME',3,7,'pez_duerme.png','lsa_pez_duerme.mp4','pez_duerme.mp4','el_pez_duerme.mp3'),(12,'EL PEZ JUEGA',3,8,'pez_juega.png','lsa_pez_juega.mp4','pez_juega.mp4','el_pez_juega.mp3'),(13,'LA VACA COME',5,6,'vaca_come.png','lsa_vaca_come.mp4','vaca_come.mp4','la_vaca_come.mp3'),(14,'LA VACA DUERME',5,7,'vaca_duerme.png','lsa_vaca_duerme.mp4','vaca_duerme.mp4','la_vaca_duerme.mp3'),(15,'LA VACA JUEGA',5,8,'vaca_juega.png','lsa_vaca_juega.mp4','vaca_juega.mp4','la_vaca_juega.mp3');
/*!40000 ALTER TABLE `sentences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `creation_date` datetime DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `profile_picture` varchar(400) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `video_visto` tinyint(1) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `tutor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `tutor_id` (`tutor_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`tutor_id`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'SERENA','VARGAS','serenavargas@escuelathays.edu.ar','scrypt:32768:8:1$vkzmifwInGVMM3WA$267805df46d20dcb1ad7cf821e5c6a94de803294615984fd55b1f509c5eabbe92f7ed5c88836971362191d955bea38746fd46d4ec54b4c1027c4f7c2164fa692','2026-08-27 18:28:26','SERENA','img/user/user.png',1,1,'child',NULL,NULL),(2,'serena','vargas','sserenavargass@gmail.com','scrypt:32768:8:1$8PGt4TxoboTwOpeG$544e06d72161b04204d1d7edf8dabb57bb66534c80e680269a10be952c973cd85b6a8b9a1d6c605b5186084614b7fc8993393313d8ccfe0f4576004559cadb82','2026-08-27 18:32:41','serenana','img/user/user.png',1,1,'tutor',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `id_word` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(100) NOT NULL,
  `articulo` varchar(10) DEFAULT NULL,
  `image_file` varchar(255) NOT NULL,
  `lsa_video_file` varchar(255) DEFAULT NULL,
  `id_category` int(11) NOT NULL,
  PRIMARY KEY (`id_word`),
  KEY `id_category` (`id_category`),
  CONSTRAINT `words_ibfk_1` FOREIGN KEY (`id_category`) REFERENCES `categories` (`id_category`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `words`
--

LOCK TABLES `words` WRITE;
/*!40000 ALTER TABLE `words` DISABLE KEYS */;
INSERT INTO `words` VALUES (1,'PERRO','EL','perro.png','perro.mp4',1),(2,'GATO','EL','gato.png','gato.mp4',1),(3,'PEZ','EL','pez.png','pez.mp4',1),(4,'P├üJARO','EL','pajarito.png','pajaro.mp4',1),(5,'VACA','LA','vaca.png','vaca.mp4',1),(6,'COMER',NULL,'comer.png','comer.mp4',2),(7,'DORMIR',NULL,'dormir.png','dormir.mp4',2),(8,'JUGAR',NULL,'jugar.png','jugar.mp4',2);
/*!40000 ALTER TABLE `words` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-27 18:57:24
